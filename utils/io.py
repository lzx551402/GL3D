#!/usr/bin/env python
"""
Copyright 2017, Zixin Luo, HKUST.
IO tools.
"""

from __future__ import print_function

from struct import unpack
import numpy as np


def read_corr(file_path):
    """Read match correspondence file.
    Args:
        file_path: file path.
    Returns:
        matches: list of match data, each consists of two image indices and Nx15 match matrix, of
        which each line consists of two 2x3 transformations, geometric distance and two feature
        indices.
    """
    matches = []
    with open(file_path, 'rb') as fin:
        while True:
            rin = fin.read(24)
            if rin == '':
                # EOF
                break
            idx0, idx1, num = unpack('L' * 3, rin)
            bytes_theta = num * 60
            corr = np.fromstring(fin.read(bytes_theta), dtype=np.float32).reshape(-1, 15)
            matches.append([idx0, idx1, corr])
    return matches


def read_kpt(file_path):
    """Read keypoint file.
    Args:
        file path: file path.
    Returns:
        kpt_data: keypoint data of Nx9 numpy array.
    """
    kpt_data = np.fromfile(file_path, dtype=np.float32)
    kpt_data = np.reshape(kpt_data, (-1, 9))
    return kpt_data
