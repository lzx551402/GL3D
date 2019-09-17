#!/usr/bin/env python
"""
Copyright 2018, Zixin Luo, HKUST.
Geometry computations.
"""

from __future__ import print_function

import numpy as np
import cv2


def interpolate_depth(pos, depth):
    ids = np.array(range(0, pos.shape[0]))

    h, w = depth.shape

    i = pos[:, 0]
    j = pos[:, 1]

    i_top_left = np.floor(i).astype(np.int32)
    j_top_left = np.floor(j).astype(np.int32)
    valid_top_left = np.logical_and(i_top_left >= 0, j_top_left >= 0)

    i_top_right = np.floor(i).astype(np.int32)
    j_top_right = np.ceil(j).astype(np.int32)
    valid_top_right = np.logical_and(i_top_right >= 0, j_top_right < w)

    i_bottom_left = np.ceil(i).astype(np.int32)
    j_bottom_left = np.floor(j).astype(np.int32)
    valid_bottom_left = np.logical_and(i_bottom_left < h, j_bottom_left >= 0)

    i_bottom_right = np.ceil(i).astype(np.int32)
    j_bottom_right = np.ceil(j).astype(np.int32)
    valid_bottom_right = np.logical_and(i_bottom_right < h, j_bottom_right < w)

    # Valid corner
    valid_corner = np.logical_and(
        np.logical_and(valid_top_left, valid_top_right),
        np.logical_and(valid_bottom_left, valid_bottom_right)
    )

    i_top_left = i_top_left[valid_corner]
    j_top_left = j_top_left[valid_corner]

    i_top_right = i_top_right[valid_corner]
    j_top_right = j_top_right[valid_corner]

    i_bottom_left = i_bottom_left[valid_corner]
    j_bottom_left = j_bottom_left[valid_corner]

    i_bottom_right = i_bottom_right[valid_corner]
    j_bottom_right = j_bottom_right[valid_corner]

    ids = ids[valid_corner]

    # Valid depth
    valid_depth = np.logical_and(
        np.logical_and(
            depth[i_top_left, j_top_left] > 0,
            depth[i_top_right, j_top_right] > 0
        ),
        np.logical_and(
            depth[i_bottom_left, j_bottom_left] > 0,
            depth[i_bottom_right, j_bottom_right] > 0
        )
    )

    i_top_left = i_top_left[valid_depth]
    j_top_left = j_top_left[valid_depth]

    i_top_right = i_top_right[valid_depth]
    j_top_right = j_top_right[valid_depth]

    i_bottom_left = i_bottom_left[valid_depth]
    j_bottom_left = j_bottom_left[valid_depth]

    i_bottom_right = i_bottom_right[valid_depth]
    j_bottom_right = j_bottom_right[valid_depth]

    ids = ids[valid_depth]

    # Interpolation
    i = i[ids]
    j = j[ids]
    dist_i_top_left = i - i_top_left.astype(np.float32)
    dist_j_top_left = j - j_top_left.astype(np.float32)
    w_top_left = (1 - dist_i_top_left) * (1 - dist_j_top_left)
    w_top_right = (1 - dist_i_top_left) * dist_j_top_left
    w_bottom_left = dist_i_top_left * (1 - dist_j_top_left)
    w_bottom_right = dist_i_top_left * dist_j_top_left

    interpolated_depth = (
        w_top_left * depth[i_top_left, j_top_left] +
        w_top_right * depth[i_top_right, j_top_right] +
        w_bottom_left * depth[i_bottom_left, j_bottom_left] +
        w_bottom_right * depth[i_bottom_right, j_bottom_right]
    )

    pos = np.stack([i, j], axis=1)
    return [interpolated_depth, pos, ids]


def downscale_positions(pos, scaling_steps=0):
    for _ in range(scaling_steps):
        pos = (pos - 0.5) / 2
    return pos


def upscale_positions(pos, scaling_steps=0):
    for _ in range(scaling_steps):
        pos = pos * 2 + 0.5
    return pos


def grid_positions(h, w):
    x_rng = range(0, w)
    y_rng = range(0, h)
    xv, yv = np.meshgrid(x_rng, y_rng)
    return np.reshape(np.stack((yv, xv), axis=-1), (-1, 2))


def relative_pose(pose0, pose1):
    """Compute relative pose.
    Args:
        pose: [R, t]
    Returns:
        rel_pose: [rel_R, rel_t]
    """
    rel_R = np.matmul(pose1[0], pose0[0].T)
    center0 = -np.matmul(pose0[1].T, pose0[0]).T
    center1 = -np.matmul(pose1[1].T, pose1[0]).T
    rel_t = np.matmul(pose1[0], center0 - center1)
    return [rel_R, rel_t]


def warp(pos0, rel_pose, depth0, K0, depth1, K1):
    def swap_axis(data):
        return np.stack([data[:, 1], data[:, 0]], axis=-1)

    z0, pos0, ids = interpolate_depth(pos0, depth0)

    uv0_homo = np.concatenate([swap_axis(pos0), np.ones((pos0.shape[0], 1))], axis=-1)
    xy0_homo = np.matmul(np.linalg.inv(K0), uv0_homo.T)
    xyz0_homo = np.concatenate([np.expand_dims(z0, 0) * xy0_homo,
                                np.ones((1, pos0.shape[0]))], axis=0)

    xyz1 = np.matmul(rel_pose, xyz0_homo)
    xy1_homo = xyz1 / np.expand_dims(xyz1[-1, :], axis=0)
    uv1 = np.matmul(K1, xy1_homo).T[:, 0:2]

    pos1 = swap_axis(uv1)
    annotated_depth, pos1, new_ids = interpolate_depth(pos1, depth1)

    ids = ids[new_ids]
    pos0 = pos0[new_ids]
    estimated_depth = xyz1.T[new_ids, -1]

    inlier_mask = np.abs(estimated_depth - annotated_depth) < 0.05

    ids = ids[inlier_mask]
    pos0 = pos0[inlier_mask]
    pos1 = pos1[inlier_mask]
    return pos0, pos1, ids


def undist_points(pts, K, dist, img_size=None):
    n = pts.shape[0]
    new_pts = pts
    if img_size is not None:
        hs = img_size / 2
        new_pts = np.stack([pts[:, 2] * hs[0] + hs[0], pts[:, 5] * hs[1] + hs[1]], axis=1)

    new_dist = np.zeros((5), dtype=np.float32)
    new_dist[0] = dist[0]
    new_dist[1] = dist[1]
    new_dist[4] = dist[2]

    upts = cv2.undistortPoints(np.expand_dims(new_pts, axis=1), K, new_dist)
    upts = np.squeeze(cv2.convertPointsToHomogeneous(upts), axis=1)
    upts = np.matmul(K, upts.T).T[:, 0:2]

    if img_size is not None:
        new_upts = pts.copy()
        new_upts[:, 2] = (upts[:, 0] - hs[0]) / hs[0]
        new_upts[:, 5] = (upts[:, 1] - hs[1]) / hs[1]
        return new_upts
    else:
        return upts


def skew_symmetric_mat(v):
    v = v.flatten()
    M = np.stack([
        (0, -v[2], v[1]),
        (v[2], 0, -v[0]),
        (-v[1], v[0], 0),
    ], axis=0)
    return M


def get_essential_mat(t0, t1, R0, R1):
    """
    Args:
        t: 3x1 mat.
        R: 3x3 mat.
    Returns:
        e_mat: 3x3 essential matrix.
    """
    dR = np.matmul(R1, R0.T)  # dR = R_1 * R_0^T
    dt = t1 - np.matmul(dR, t0)  # dt = t_1 - dR * t_0

    dt = dt.reshape(1, 3)
    dt_ssm = skew_symmetric_mat(dt)

    e_mat = np.matmul(dt_ssm, dR)  # E = dt_ssm * dR
    e_mat = e_mat / np.linalg.norm(e_mat)
    return e_mat


def get_epipolar_dist(kpt_coord0, kpt_coord1, K0, K1, ori_img_size0, ori_img_size1, e_mat, eps=1e-6):
    """
    Compute (symmetric) epipolar distances.
    Args:
        kpt_coord: Nx2 keypoint coordinates, normalized to [-1, +1].
        K: 3x3 intrinsic matrix.
        ori_img_size: original image size (width, height)
        e_mat: Precomputed essential matrix.
        get_epi_dist_mat: Whether to get epipolar distance in matrix form or vector form.
        eps: Epsilon.
    Returns:
        epi_dist: N-d epipolar distance.
    """
    def _get_homo_coord(coord):
        homo_coord = np.concatenate([coord, np.ones_like(coord[:, 0, None])], axis=-1)
        return homo_coord
        
    uv0_homo = _get_homo_coord(kpt_coord0 * ori_img_size0 / 2 + ori_img_size0 / 2)
    uv1_homo = _get_homo_coord(kpt_coord1 * ori_img_size1 / 2 + ori_img_size1 / 2)
    # normalize keypoint coordinates with camera intrinsics.
    xy0_homo = np.matmul(np.linalg.inv(K0), uv0_homo.T)
    xy1_homo = np.matmul(np.linalg.inv(K1), uv1_homo.T)
    # epipolar lines in the first image.
    Ex0 = np.matmul(e_mat, xy0_homo)  # Bx3xN
    # epipolar lines in the second image.
    Etx1 = np.matmul(e_mat.T, xy1_homo) # Bx3xN
    # get normal vectors.
    line_norm0 = Ex0[0, :] ** 2 + Ex0[1, :] ** 2
    line_norm1 = Etx1[0, :] ** 2 + Etx1[1, :] ** 2
    x1Ex0 = np.sum(xy1_homo * Ex0, axis=0)
    epi_dist = (x1Ex0 ** 2) / (line_norm0 + line_norm1 + eps)
    epi_dist = np.sqrt(epi_dist)
    return epi_dist