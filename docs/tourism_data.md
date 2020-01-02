![Example sequence](../imgs/tourism_view.png)

## Dataset Description

One potential shortcoming of GL3D is that images are captured within a short period of time, thus lack of illumination/weather/season variations. Although photometric data augmentation could be applied, we still seek for more realistic data to improve the learning models.

To this end, following SiaMAC [\[1\]][1], we have also generated geometric labels from public Internet tourism datasets to further increase the data diversity. Precisely, we download and extract the images from [retrieval-SfM-120k.mat](http://cmp.felk.cvut.cz/cnnimageretrieval/), then reconstruct each data by our 3D engine, and finally obtain 530 scenes (55,657 images) that we consider are well-constructed (> 80% images are registered).

## Downloads

The same protocols are defined for downloading the data. For dataset images:

| Sources |    Data Name   | Chunk Start | Chunk End | Disk |       Descriptions       |
|:-------:|:--------------:|:-----------:|:---------:|:----:|:------------------------:|
|  tourism|tourism_raw_imgs|      0      |    38     | 19G  |Original images of tourism dataset  |
|  tourism|tourism_imgs    |      0      |    29     | 15G  |1000x1000 undistorted images of tourism dataset|

For geometric labels:

|File Name                  |Data Name|Chunk Start|Chunk End|Disk |Task  |
|:--------------------------|:-------:|:---------:|:-------:|:---:|:----:|
|geolabel/cameras.txt       |tourism_cams |0         |0     |<0.1G|Common|
|img_kpts/<img_idx>.bin     |tourism_kpts|0          |12    |6.0G |Common|
|depths/<img_idx>.pfm       |tourism_depths|0        |24    |12G  |Common|
|geolabel/corr.bin          |tourism_corr|0          |9     |4.5G |Local descriptor|
|geolabel/mask.bin          |tourism_mask|0          |13    |6.5G |Image retrieval|
|geolabel/common_track.txt  |tourism_ct  |0          |0     |<0.1G|Image retrieval|
|geolabel/mesh_overlap.txt  |tourism_mo  |0          |0     |<0.1G|Image retrieval|

[1]: https://arxiv.org/abs/1604.02426