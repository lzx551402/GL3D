#!/usr/bin/env python
"""
Copyright 2017, Zixin Luo, HKUST.
IO tools.
"""

from __future__ import print_function

from struct import unpack
import numpy as np


def read_corr(file_path):
    """Read the match correspondence file.
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
    """Read the keypoint file.
    Args:
        file path: file path.
    Returns:
        kpt_data: keypoint data of Nx9 numpy array.
    """
    kpt_data = np.fromfile(file_path, dtype=np.float32)
    kpt_data = np.reshape(kpt_data, (-1, 9))
    return kpt_data


def hash_int_pair(ind1, ind2):
    """Hash an int pair.
    Args:
        ind1: int1.
        ind2: int2.
    Returns:
        hash_index: the hash index.
    """
    assert ind1 <= ind2
    return ind1 * 2147483647 + ind2


def read_mask(file_path, size=14):
    """Read the mask file.
    Args:
        file_path: file path.
        size: mask size.
    Returns:
        mask_dict: mask data in dictionary, indexed by hashed pair index.
    """
    mask_dict = {}
    size = size * size * 2
    record_size = 8 + size

    with open(file_path, 'rb') as fin:
        data = fin.read()
    for i in range(0, len(data), record_size):
        decoded = unpack('Q' + '?' * size, data[i: i + record_size])
        mask = np.array(decoded[1:])
        mask_dict[decoded[0]] = mask
    return mask_dict
