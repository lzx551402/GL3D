![Example sequence](../imgs/tourism_view.png)

## Dataset Description

Following SiaMAC [\[1\]][1], we have also generated geometric labels from public Internet tourism datasets to further increase the data diversity. Precisely, we download and extract the images from [retrieval-SfM-120k.mat](http://cmp.felk.cvut.cz/cnnimageretrieval/), reconstruct each data by our 3D engine, and finally obtain 530 scenes (55,657 images) of sufficent number of registered images (e.g., > 80%).

## Downloads

The same protocols are defined for downloading the data.

|File Name                  |Data Name|Chunk Start|Chunk End|
|:--------------------------|:-------:|:---------:|:-------:|
|undist_images/<img_idx>.jpg|tourism_imgs |0         |29    |
|geolabel/cameras.txt       |tourism_cams |0         |0     |
|img_kpts/<img_idx>.bin     |tourism_kpts|0          |12    |
|depths/<img_idx>.pfm       |tourism_depths|0        |24    |
|geolabel/corr.bin          |tourism_corr|0          |9     |
|geolabel/mask.bin          |tourism_mask|0          |13    |
|geolabel/common_track.txt  |tourism_ct  |0          |0     |
|geolabel/mesh_overlap.txt  |tourism_mo  |0          |0     |

[1]: https://arxiv.org/abs/1604.02426