## geolabel/cameras.txt
This file contains the intrisic/extrinsic parameters of cameras.

```
# One line of data per image:
# IMAGE_ID, FX, FY, PX, PY, SKEW, TRANSLATION VECTOR (3x1), ROTATION MATRIX (3x3), RADIAL DISTORTION (3x1), IMAGE SIZE (2x1).

0 3995.67 3995.67 2304 1728 0 63.6722 -28.8643 53.9166 0.919771 -0.39198 0.0192924 -0.390128 -0.918559 -0.0636394 0.0426665 0.0510072 -0.997786 0.0131149 0.0165777 -0.0248811 4608 3456
1 3995.67 3995.67 2304 1728 0 42.5446 -29.6565 53.7087 0.920426 -0.390256 0.0227155 -0.387471 -0.91847 -0.0792399 0.0517874 0.0641329 -0.996597 0.0131149 0.0165777 -0.0248811 4608 3456
2 3995.67 3995.67 2304 1728 0 -0.670276 -46.8927 76.4343 0.587792 0.0768202 0.805356 -0.632594 -0.576902 0.51673 0.504307 -0.813193 -0.290502 0.0131149 0.0165777 -0.0248811 4608 3456
...
```

## img_kpts/<img_idx>.bin
This file contains the 2D keypoints detected by SIFT from the corresponding images. Each keypoint is parameterized by a 2x3 transformation, composed of
keypoint position, canonical orientation and size of the support region.
Please refer to [GeoDesc](https://arxiv.org/abs/1807.06294) in Sec.3.2 for the motivation of such parameterization and implementation details.

```
# One line of data per keypoint in float32:
# TRANSFORMATION (2x3)

-0.25711258 0.52153266 -0.58181703 -0.78229898 -0.38566887 -0.53048758
0.02235542 0.56109281 0.36527826 -0.84163922 0.03353313 -0.26430511
...
```

Given image size (W, H), the keypoint position can be obtained by:
```
(x, y) = (TRANSFORMATION[0, 2] * W/2 + W/2, TRANSFORMATION[1, 2] * H/2 + H/2)
```

Be noted that the keypoints are detected from distorted images. The undistortion function is provided in [geom.py](../utils/geom.py) and example usage can be found in [example.py](../example/visualize.py).

## depths/.pfm (not ready)
Depth maps are stored in pfm format. Use `load_pfm` in [io.py](../utils/io.py) to prase the data.

## geolabel/corr.bin
This file contains the image matching results for the entire scene data.
```
# One line of data header per matching record, followed by several lines of correspondences records.
# (header) IMG_IDX0, IMG_IDX1, CORR_NUM (in int64)
# (corr0) TRANSFORMATION0 (2x3), TRANSFORMATION1 (2x3), GEOMETRIC DISTANCE, FEATURE_IDX0, FEATURE_IDX1 (in float32)
# (corr1) ...
# ...

0 31
-0.08972209 0.00347713 0.2302869 -0.0052157 -0.13458313 0.41775447 \
-0.09017891 -0.00771412 0.12965393 0.01157118 -0.13526838 0.7921493 \
0.06584082 167. 142.        
...
```

`FEATURE_IDX` corresponds to the line index of the keypoint files.

## geolabel/common_track.txt & geolabel/mesh_overlap.txt (not ready)
This file contains the overlap ratio of image pairs computed from common track ratio or mesh re-projections.
```
# One line of data per data:
1 20 0.447471
20 1 0.0652112
...
```

Be noted that the both measurements are not symmetrical.

## geolabel/mask.bin (not ready)
This file contains the overlap masks of image pairs, which have the resolution of 14x14.
Each mask record has an unique index, hashed from the image pair index. Specifically, 
*mask_index = image_index0 * 2147483647 + image_index1*, where *image_index0 <= image_index1*.
```
# One line of data per mask record, started by a hashed pair index (int64) then followed by two mask record of an image pair (14x14x2 bool).
# HASHED INDEX, MASK RECORD0 (14x14), MASK RECORD1 (14x14)
2 false false false true true true true true ... (for the first image) false false false false ... (for the second image)
...
```

`true` indicates overlapping region.

