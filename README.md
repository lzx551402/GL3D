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

If you have used the correspondence labels, please also cite:

    @inproceedings{luo2018geodesc,
        title={Geodesc: Learning local descriptors by integrating geometry constraints},
        author={Luo, Zixin and Shen, Tianwei and Zhou, Lei and Zhu, Siyu and Zhang, Runze and Yao, Yao and Fang, Tian and Quan, Long},
        booktitle={European Conference on Computer Vision (ECCV)},
        year={2018}
    }

## Dataset Description

GL3D contains 125,623 high-resolution images regarding 543 different scenes. 
Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline. 
Refer to [\[1\]][1] for details. 
For each scene data, we provide the complete image sequence, geometric labels and reconstruction results.

## Tasks

Research works below are supported by GL3D:

|Task            |Reference                                           |
|:--------------:|:--------------------------------------------------:|
|Image retrieval |[MIRorR](https://arxiv.org/abs/1811.10343), ACCV'18 |
|Local descriptor|[GeoDesc](https://arxiv.org/abs/1807.06294), ECCV'18|
|Local descriptor|[ContextDesc](https://arxiv.org/abs/1904.04084), CVPR'19|

## Download

Undistorted images resized to 1000x1000 are provided.

| Sources |    Data Name   | Chunk Start | Chunk End |       Descriptions       |
|:-------:|:--------------:|:-----------:|:---------:|:------------------------:|
|   GL3D  |    gl3d_imgs   |      0      |    125    | 1000x1000 images of GL3D |

Use `download_data.sh` script to download the tar files, by passing augments
```
bash download_data.sh <data_name> <chunk_start> <chunk_end>
```
For example, to download GL3D images, run
```
bash download_data.sh gl3d_imgs 0 125
```

To extract the files, run
```
cat download_data_gl3d_imgs/*.tar.* | tar -xvf - -z
```

## Dataset Format 

```
data                          
 └── <pid> 
       ├── undist_images/*
       ├── geolabel/*
       ├── img_kpts/*.bin
       └── image_list.txt
```

|File Name                |Data Name|Chunk Start|Chunk End|Task            |Descriptions                                                           |
|:------------------------|:-------:|:---------:|:-------:|:--------------:|:---------------------------------------------------------------------:|
|geolabel/cameras.txt     |gl3d_cams |0          |0        |Common          |Camera intrisic/extrinsic parameters, recovered by SfM.                |
|img_kpts/<img_idx>.bin   |gl3d_kpts|0          |57       |Common          |Image keypoints detected by SIFT.                                      |
|depths/<img_idx>.pfm     |gl3d_depths|0        |59       |Local descriptor|Depth maps.                    |
|geolabel/corr.bin        |gl3d_corr|0          |12       |Local descriptor|Image correspondences that haved survived from SfM.                    |
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

## Changelog
### 2019-9-17 Releasing of GL3D_V2
- Another 165 datasets are added, covering mainly landmarks and small objects.
- Rerun SfM for all datasets with [GeoDesc](https://github.com/lzx551402/geodesc) to obtain denser reconstruction.
- Camera distortion paramters are provided.
- Undistorted images are provided.
- More helper functions to perform geometry computation.
<<<<<<< HEAD

### 2019-12-4 Update GL3D_V2
- Provide depth maps to enrich geometric labels.
- Provide helper functions to parse depth maps.
=======
>>>>>>> 0da15fc601183a31f248ade9a3acdcc791f1b367
