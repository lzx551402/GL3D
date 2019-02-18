# GL3D: Geometric Learning with 3D Reconstruction
![Example sequence](img/dataset_view.png)

## About

**GL3D** (Geometric Learning with 3D Reconstruction) is a large-scale database created for 3D reconstruction and geometry-related learning problems. Most images contained are captured by drones from multiple scales and perspectives with large geometric overlaps, covering urban, rural area, or scenic spots. It also includes small object reconstructions to enrich the data diversity. If you find this dataset useful for your research, please cite:

    @inproceedings{shen2018mirror,
        author={Shen, Tianwei and Luo, Zixin and Zhou, Lei and Zhang, Runze and Zhu, Siyu and Fang, Tian and Quan, Long},
        title={Matchable Image Retrieval by Learning from Surface Reconstruction},
        booktitle={The Asian Conference on Computer Vision (ACCV},
        year={2018},
    }

## Dataset Description

GL3D contains 90,630 high-resolution images regarding 378 different scenes. 
Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline. 
Refer to [\[1\]][1] for details. 
For each scene data, we provide the complete image sequence, geometric labels and reconstruction results.

## Tasks

Research works below are supported by GL3D:

|Task            |Reference                                           |
|:--------------:|:--------------------------------------------------:|
|Image retrieval |[MIRorR](https://arxiv.org/abs/1811.10343), ACCV'18 |
|Local descriptor|[GeoDesc](https://arxiv.org/abs/1807.06294), ECCV'18|

## Download

For image retrieval task, use 224x224 images and refer to [MIRorR](https://github.com/hlzz/mirror).

For learning local descriptor, use 1000x1000 images and refer to [GeoDesc](https://github.com/lzx551402/geodesc).

| Sources |    Data Name   | Chunk Start | Chunk End |       Descriptions       |
|:-------:|:--------------:|:-----------:|:---------:|:------------------------:|
|   GL3D  | gl3d_full_size |     TBA     |    TBA    | Full-size images of GL3D |
|   GL3D  |    gl3d_224    |      0      |     6     |  224x224 images of GL3D  |
|   GL3D  |    gl3d_1000   |      0      |     91    | 1000x1000 images of GL3D |

Use `download_data.sh` script to download the tar files, by passing augments
```
bash download_data.sh <data_name> <chunk_start> <chunk_end>
```
For example, to download GL3D 224x224 images, run
```
bash download_data.sh gl3d_224 0 6 
```

To extract the files, run
```
cat download_data_gl3d_224/*.tar.* | tar -xvf -
```

## Dataset Format 

```
data                          
 └── <pid> 
       ├── images/*
       ├── geolabel/*
       ├── img_kpts/*.bin
       └── image_list.txt
```

|File Name                |Data Name|Chunk Start|Chunk End|Task            |Descriptions                                                           |
|:------------------------|:-------:|:---------:|:-------:|:--------------:|:---------------------------------------------------------------------:|
|geolabel/cameras.txt     |gl3d_cams|0          |0        |Common          |Camera intrisic/extrinsic parameters, recovered by SfM.                |
|img_kpts/<img_idx>.bin   |gl3d_kpts|0          |58       |Common          |Image keypoints detected by SIFT.                                      |
|geolabel/corr.bin        |gl3d_corr|0          |7        |Local descriptor|Image correspondences that haved survived from SfM.                    |
|geolabel/mask.bin        |gl3d_mask|0          |8        |Image retrieval |Overlap masks of image pairs, computed from mesh re-projections.       |
|geolabel/mesh_overlap.txt|gl3d_mo  |0          |0        |Image retrieval |Mesh overlap ratio of image pairs, computed from mesh re-projections.  |
|geolabel/common_track.txt|gl3d_ct  |0          |0        |Image retrieval |Common track ratio of image pairs, computed from SfM.                  |

Again, use `download_data.sh` to fetch the above geometric labels or reconstruction results, 

For data organization, refer to [docs/format.md](doc/format.md).

Python-based IO utilities are provided to parse the data, refer to [utils/io.py](utils/io.py).

Visualizations and examples of usage can be found in [example/README.md](example/README.md).

Please feel free to inform us if you need some other intermediate results for your research.

## Data Preview
The mesh reconstruction is available for preview by substituting `<pid>` in the following link:

```
https://www.altizure.com/project-model?pid=<pid>
```

An example is provided [here](https://www.altizure.com/project-model?pid=57f8d9bbe73f6760f10e916a).
Noted that some projects are not online available, from `000000000000000000000000` to `00000000000000000000001d`.

## Acknowledgments
This dataset is prepared and maintained by
[Zixin Luo](mailto:zluoag@cse.ust.hk),
[Tianwei Shen](mailto:tshenaa@cse.ust.hk),
[Jacky Tang](mailto:jackytck@gmail.com) and
[Tian Fang](mailto:fangtian@altizure.com).
3D reconstructions are obtained by [Altizure](https://www.altizure.com/).

[1]: https://arxiv.org/abs/1811.10343