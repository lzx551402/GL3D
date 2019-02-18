#!/usr/bin/env python
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

from utils.io import read_kpt, read_corr, read_mask, hash_int_pair


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
    args = parser.parse_args()

    img_path0 = os.path.join('data', 'images', 'DJI_0348.JPG')
    img_path1 = os.path.join('data', 'images', 'DJI_0350.JPG')

    img0 = cv2.imread(img_path0)[..., ::-1]
    img1 = cv2.imread(img_path1)[..., ::-1]

    if args.fn == 'kpt':
        # visualize the keypoint file.
        kpt_path0 = os.path.join('data', 'img_kpts', '0.bin')
        kpt_path1 = os.path.join('data', 'img_kpts', '2.bin')
        kpts0 = read_kpt(kpt_path0)
        kpts0 = np.stack([kpts0[:, 2], kpts0[:, 5]], axis=-1)
        img_size0 = np.array((img0.shape[1], img0.shape[0]))
        kpts0 = kpts0 * img_size0 / 2 + img_size0 / 2

        kpts1 = read_kpt(kpt_path1)
        kpts1 = np.stack([kpts1[:, 2], kpts1[:, 5]], axis=-1)
        img_size1 = np.array((img1.shape[1], img1.shape[0]))
        kpts1 = kpts1 * img_size1 / 2 + img_size1 / 2

        display = draw_kpts([img0, img1], [kpts0, kpts1])
    elif args.fn == 'match':
        # visualize the correspondence file.
        corr_path = os.path.join('data', 'geolabel', 'corr.bin')
        match_records = read_corr(corr_path)
        kpts0 = np.stack([match_records[0][2][:, 2], match_records[0][2][:, 5]], axis=-1)
        img_size0 = np.array((img0.shape[1], img0.shape[0]))
        kpts0 = kpts0 * img_size0 / 2 + img_size0 / 2

        kpts1 = np.stack([match_records[0][2][:, 8], match_records[0][2][:, 11]], axis=-1)
        img_size1 = np.array((img1.shape[1], img1.shape[0]))
        kpts1 = kpts1 * img_size1 / 2 + img_size1 / 2

        match_num = kpts0.shape[0]
        match_idx = np.tile(np.array(range(match_num))[..., None], [1, 2])

        display = draw_matches(img0, img1, kpts0, kpts1, match_idx, downscale_ratio=0.05)
    elif args.fn == 'mask':
        # visualize the mask file.
        mask_path = os.path.join('data', 'geolabel', 'mask.bin')
        mask_dict = read_mask(mask_path)
        mask = mask_dict.get(hash_int_pair(0, 2))

        display = draw_mask(img0, img1, mask, downscale_ratio=0.2)
    else:
        raise NotImplementedError()

    plt.xticks([])
    plt.yticks([])
    plt.imshow(display)
    plt.show()
