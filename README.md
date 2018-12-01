# GL3D: Geometric Learning with 3D Reconstruction
![Example sequence](img/dataset_view.png)

## About

**GL3D** (Geometric Learning with 3D Reconstruction) is a large-scale database created for 3D reconstruction and geometry-related learning problems. Most images contained are captured by drones from multiple scales and perspectives with large geometric overlaps, covering urban, rural area, or scenic spots. It also includes small object data to enrich the data diversity. If you find this dataset useful for your research, please cite:

    @inproceedings{shen2018mirror,
        author={Shen, Tianwei and Luo, Zixin and Zhou, Lei and Zhang, Runze and Zhu, Siyu and Fang, Tian and Quan, Long},
        title={Matchable Image Retrieval by Learning from Surface Reconstruction},
        booktitle={The Asian Conference on Computer Vision (ACCV},
        year={2018},
    }

## Dataset Description

GL3D contains 90,630 high-resolution images regarding 378 different scenes. Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline. Refer to [\[1\]][1] for details. For each scene data, we provide the complete image sequence, geometric labels.

## Download

To train the retrieval model, use 224x224 images and refer to [MIRorR](https://github.com/hlzz/mirror).

To train the local descriptor, use 1000x1000 images and refer to [GeoDesc](https://github.com/lzx551402/geodesc).

|  Sources | Full size |  224x224 | 1000x1000 |
|:--------:|:---------:|:--------:|:---------:|
| GL3D     | [TBA]() | [3.3 GB]() | [45.0 GB]() |

## Dataset Format 

```
data                          
 └── <pid> 
       ├── images       
       ├── geolabel
       ├── img_kpts 
       └── image_list.txt
```

|File Name                |Task            |Format|Descriptions                                |Dowload |
|:------------------------|:--------------:|:----:|:------------------------------------------:|:------:|
|img_kpts/<img_id>.parsed |Local descriptor|      |Image keypoints detected by SIFT            |[TBA]()|
|geolabel/corr.bin        |Local descriptor|      |Image correspondences that have survived SfM|[TBA]()|
|geolabel/mask.bin        |Image retrieval |      |                                            |[TBA]()|
|geolabel/overlap_rank.txt|Image retrieval |      |The *combining overlap ratio* between images as defined in [\[1\]][1]|[TBA]()|

The mesh reconstruction is available for preview by substituting `<pid>` in the following link:

```
https://www.altizure.com/project-model?pid=<pid>
```

An example is provided [here](https://www.altizure.com/project-model?pid=57f8d9bbe73f6760f10e916a).

[1]: https://arxiv.org/abs/1811.10343