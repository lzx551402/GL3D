#!/usr/bin/env python3
"""
Copyright 2019, Zixin Luo, HKUST.
Visualization tools.
"""

from __future__ import print_function

import os
import sys
import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

sys.path.append('..')

from utils.geom import get_essential_mat, get_epipolar_dist, undist_points, warp, grid_positions, upscale_positions, downscale_positions, relative_pose
from utils.io import read_kpt, read_corr, read_mask, hash_int_pair, read_cams, load_pfm


def draw_kpts(imgs, kpts, color=(0, 255, 0), radius=2, thickness=2):
    """
    Args:
        imgs: color images.
        kpts: Nx2 numpy array.
    Returns:
        all_display: image with drawn keypoints.
    """
    all_display = []
    for idx, val in enumerate(imgs):
        kpt = kpts[idx]
        tmp_img = val.copy()
        for kpt_idx in range(kpt.shape[0]):
            display = cv2.circle(
                tmp_img, (int(kpt[kpt_idx][0]), int(kpt[kpt_idx][1])), radius, color, thickness)
        all_display.append(display)
    all_display = np.concatenate(all_display, axis=1)
    return all_display


def draw_matches(img0, img1, kpts0, kpts1, match_idx,
                 downscale_ratio=1, color=(0, 255, 0), radius=4, thickness=2):
    """
    Args:
        img: color image.
        kpts: Nx2 numpy array.
        match_idx: Mx2 numpy array indicating the matching index.
    Returns:
        display: image with drawn matches.
    """
    resize0 = cv2.resize(
        img0, (int(img0.shape[1] * downscale_ratio), int(img0.shape[0] * downscale_ratio)))
    resize1 = cv2.resize(
        img1, (int(img1.shape[1] * downscale_ratio), int(img1.shape[0] * downscale_ratio)))

    rows0, cols0 = resize0.shape[:2]
    rows1, cols1 = resize1.shape[:2]

    kpts0 *= downscale_ratio
    kpts1 *= downscale_ratio

    display = np.zeros((max(rows0, rows1), cols0 + cols1, 3))
    display[:rows0, :cols0, :] = resize0
    display[:rows1, cols0:(cols0 + cols1), :] = resize1

    for idx in range(match_idx.shape[0]):
        val = match_idx[idx]
        pt0 = (int(kpts0[val[0]][0]), int(kpts0[val[0]][1]))
        pt1 = (int(kpts1[val[1]][0]) + cols0, int(kpts1[val[1]][1]))

        cv2.circle(display, pt0, radius, color, thickness)
        cv2.circle(display, pt1, radius, color, thickness)
        cv2.line(display, pt0, pt1, color, thickness)

    display /= 255

    return display


def draw_mask(img0, img1, mask, size=14, downscale_ratio=1):
    """
    Args:
        img: color image.
        mask: 14x28 mask data.
        size: mask size.
    Returns:
        display: image with mask.
    """
    resize_imgs = []
    resize_imgs.append(cv2.resize(
        img0, (int(img0.shape[1] * downscale_ratio), int(img0.shape[0] * downscale_ratio))))
    resize_imgs.append(cv2.resize(
        img1, (int(img1.shape[1] * downscale_ratio), int(img1.shape[0] * downscale_ratio))))

    masks = []
    masks.append(ndimage.binary_fill_holes(np.reshape(mask[:size * size], (size, size))))
    masks.append(ndimage.binary_fill_holes(np.reshape(mask[size * size:], (size, size))))

    for idx, val in enumerate(masks):
        h_interval = np.ceil(float(resize_imgs[idx].shape[0]) / val.shape[0])
        w_interval = np.ceil(float(resize_imgs[idx].shape[1]) / val.shape[1])

        for i in range(resize_imgs[idx].shape[0]):
            for j in range(resize_imgs[idx].shape[1]):
                p = int(np.floor(i / h_interval))
                q = int(np.floor(j / w_interval))
                if val[p, q]:
                    resize_imgs[idx][i, j, 0] = 255

    display = np.concatenate(resize_imgs, axis=1)
    return display


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('fn', type=str, help='visualization function, e.g., kpt, match, mask.')
    parser.add_argument('--pair_idx', dest='pair_idx', type=int,
                        default=0, help='pair index to visualize')
    args = parser.parse_args()

    root = '../data/57f8d9bbe73f6760f10e916a'

    # read correspondences
    match_pair_idx = args.pair_idx
    corr_path = os.path.join(root, 'geolabel', 'corr.bin')
    match_records = read_corr(corr_path)
    cidx0 = match_records[match_pair_idx][0]
    cidx1 = match_records[match_pair_idx][1]
    basename0 = str(cidx0).zfill(8)
    basename1 = str(cidx1).zfill(8)
    # read images
    img_path0 = os.path.join(root, 'undist_images', basename0 + '.jpg')
    img_path1 = os.path.join(root, 'undist_images', basename1 + '.jpg')
    img0 = cv2.imread(img_path0)[..., ::-1]
    img1 = cv2.imread(img_path1)[..., ::-1]
    # read cameras
    cam_path = os.path.join(root, 'geolabel', 'cameras.txt')
    cam_dict = read_cams(cam_path)
    cam0, cam1 = cam_dict[cidx0], cam_dict[cidx1]
    K0, K1 = cam0[0], cam1[0]
    p0f0 = [(K0[0, 2], K0[1, 2]), (K0[0, 0], K0[1, 1])]
    p1f1 = [(K1[0, 2], K1[1, 2]), (K1[0, 0], K1[1, 1])]
    t0, t1 = cam0[1], cam1[1]
    R0, R1 = cam0[2], cam1[2]
    dist0, dist1 = cam0[3], cam1[3]
    ori_img_size0, ori_img_size1 = cam0[4], cam1[4]

    if args.fn == 'kpt':
        # visualize the keypoint file.
        kpt_path0 = os.path.join(root, 'img_kpts', basename0 + '.bin')
        kpt_path1 = os.path.join(root, 'img_kpts', basename1 + '.bin')
        # parse keypoint file.
        kpts0, kpts1 = read_kpt(kpt_path0), read_kpt(kpt_path0)
        # undistortion.
        kpts0 = undist_points(kpts0, K0, dist0, ori_img_size0)
        kpts1 = undist_points(kpts1, K1, dist1, ori_img_size1)
        # extract normalized coordinates.
        kpts0 = np.stack([kpts0[:, 2], kpts0[:, 5]], axis=-1)
        kpts1 = np.stack([kpts1[:, 2], kpts1[:, 5]], axis=-1)
        # get image coordinates.
        img_size0 = np.array((img0.shape[1], img0.shape[0]))
        img_size1 = np.array((img1.shape[1], img1.shape[0]))
        kpts0 = kpts0 * img_size0 / 2 + img_size0 / 2
        kpts1 = kpts1 * img_size1 / 2 + img_size1 / 2
        display = draw_kpts([img0, img1], [kpts0, kpts1])
    elif args.fn == 'match':
        kpts0 = match_records[match_pair_idx][2][:, 0:6]
        kpts0 = undist_points(kpts0, K0, dist0, ori_img_size0)
        kpts0 = np.stack([kpts0[:, 2], kpts0[:, 5]], axis=-1)

        kpts1 = match_records[match_pair_idx][2][:, 6:12]
        kpts1 = undist_points(kpts1, K0, dist1, ori_img_size1)
        kpts1 = np.stack([kpts1[:, 2], kpts1[:, 5]], axis=-1)

        # validate epipolar geometry
        e_mat = get_essential_mat(t0, t1, R0, R1)
        epi_dist = get_epipolar_dist(kpts0, kpts1, K0, K1, ori_img_size0, ori_img_size1, e_mat)
        print('max epipolar distance', np.max(epi_dist))

        img_size0 = np.array((img0.shape[1], img0.shape[0]))
        img_size1 = np.array((img1.shape[1], img1.shape[0]))
        kpts0 = kpts0 * img_size0 / 2 + img_size0 / 2
        kpts1 = kpts1 * img_size1 / 2 + img_size1 / 2
        match_num = kpts0.shape[0]
        match_idx = np.tile(np.array(range(match_num))[..., None], [1, 2])
        display = draw_matches(img0, img1, kpts0, kpts1, match_idx, downscale_ratio=1.0)
    elif args.fn == 'depth':
        depth_path0 = os.path.join(root, 'depths', basename0 + '.pfm')
        depth_path1 = os.path.join(root, 'depths', basename1 + '.pfm')
        depth0 = load_pfm(depth_path0)
        depth1 = load_pfm(depth_path1)

        rel_pose = relative_pose([R0, t0], [R1, t1])
        rel_pose = np.concatenate(rel_pose, axis=-1)

        pos0 = grid_positions(depth0.shape[0], depth0.shape[1])
        r0 = ori_img_size0 / depth0.shape[::-1][1:]
        r1 = ori_img_size1 / depth1.shape[::-1][1:]
        r_K0 = np.stack([K0[0] / r0[0], K0[1] / r0[1], K0[2]], axis=0)
        r_K1 = np.stack([K1[0] / r1[0], K1[1] / r1[1], K1[2]], axis=0)

        pos0, pos1, ids = warp(pos0, rel_pose, depth0, r_K0, depth1, r_K1)

        disp_img0 = cv2.resize(img0, (0, 0), fx=0.25, fy=0.25)
        disp_img1 = cv2.resize(img1, (0, 0), fx=0.25, fy=0.25)

        pos0 = np.round(pos0).astype(np.int32)
        pos1 = np.round(pos1).astype(np.int32)

        warp_img = np.zeros_like(disp_img1)
        warp_img[pos1[:, 0], pos1[:, 1]] = disp_img0[pos0[:, 0], pos0[:, 1]]
        display = np.concatenate([warp_img, disp_img1], axis=1)
    else:
        raise NotImplementedError()

    plt.xticks([])
    plt.yticks([])
    plt.imshow(display)
    plt.show()
