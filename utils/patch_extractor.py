#!/usr/bin/env python
"""
Copyright 2018, Zixin Luo, HKUST.
OpenCV helper.
"""

from __future__ import print_function

import numpy as np
import cv2


class PatchExtractor(object):
    """"OpenCV SIFT wrapper."""

    def __init__(self, patch_size=32):
        self.patch_size = patch_size

    def get_interest_region(self, gray_img, kpts):
        """Get the interest region around a keypoint.
        Args:
            gray_img: Grayscale input image.
            kpts: Nx6 keypoint transformation.
        Returns:
            all_patches: An array of patches of Nx32x32.
        """

        kpt_n = kpts.shape[0]
        H = gray_img.shape[0]
        W = gray_img.shape[1]
        batch_input_grid = []
        all_patches = []
        bs = 30  # limited by OpenCV remap implementation
        for idx in range(kpt_n):
            # construct affine transformation matrix.
            affine_mat = np.zeros((3, 2), dtype=np.float32)
            affine_mat[0, 0] = kpts[idx, 0] * W
            affine_mat[1, 0] = kpts[idx, 1] * W
            affine_mat[2, 0] = kpts[idx, 2] * W / 2 + W / 2
            affine_mat[0, 1] = kpts[idx, 3] * H
            affine_mat[1, 1] = kpts[idx, 4] * H
            affine_mat[2, 1] = kpts[idx, 5] * H / 2 + H / 2
            # get input grid.
            input_grid = np.matmul(self.output_grid, affine_mat)
            input_grid = np.reshape(input_grid, (-1, 1, 2))
            batch_input_grid.append(input_grid)

            if len(batch_input_grid) != 0 and len(batch_input_grid) % bs == 0 or idx == kpt_n - 1:
                # sample image pixels.
                batch_input_grid_ = np.concatenate(batch_input_grid, axis=0)
                patches = cv2.remap(gray_img.astype(np.float32), batch_input_grid_,
                                    None, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                patches = np.reshape(patches, (len(batch_input_grid),
                                               self.patch_size, self.patch_size))
                all_patches.append(patches)
                batch_input_grid = []
        if len(all_patches) != 0:
            all_patches = np.concatenate(all_patches, axis=0)
        else:
            all_patches = None
        return all_patches

    def get_patches(self, gray_img, kpts):
        """Get all patches around given keypoints.
        Args:
            cv_kpts: A list of keypoints represented as cv2.KeyPoint.
        Return:
            all_patches: (n_kpts, 32, 32) Cropped patches.
        """

        # generate sampling grids.
        n_pixel = np.square(self.patch_size)
        self.output_grid = np.zeros((n_pixel, 3), dtype=np.float32)
        for i in range(n_pixel):
            self.output_grid[i, 0] = (i % self.patch_size) * 1. / self.patch_size * 2 - 1
            self.output_grid[i, 1] = (i // self.patch_size) * 1. / self.patch_size * 2 - 1
            self.output_grid[i, 2] = 1

        all_patches = self.get_interest_region(gray_img, kpts)
        return all_patches
