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

GL3D contains 90,630 high-resolution images regarding 378 different scenes. Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline. Refer to [\[1\]][1] for details. For each scene data, we provide the complete image sequence and geometric labels.

## Download

For image retrieval task, use 224x224 images and refer to [MIRorR](https://github.com/hlzz/mirror).

For learning local descriptor, use 1000x1000 images and refer to [GeoDesc](https://github.com/lzx551402/geodesc).

| Sources |    Data Name   | Chunk Start | Chunk End |       Descriptions       |
|:-------:|:--------------:|:-----------:|:---------:|:------------------------:|
|   GL3D  | gl3d_full_size |     TBA     |    TBA    | Full-size images of GL3D |
|   GL3D  |    gl3d_224    |      0      |     6     |  224x224 images of GL3D  |
|   Gl3D  |    gl3d_1000   |      0      |     91    | 1000x1000 images of GL3D |

Use `download_data.sh` script to download the tar files, by passing augments
```
bash download_data.sh <data_name> <chunk_start> <chunk_end>
```
For example, to download GL3D 224x224 images, run
```
bash download_data.sh gl3d_224 0 6 
```

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
|img_kpts/<img_id>.parsed |Local descriptor|TBA      |TBA|TBA|
|geolabel/corr.bin        |Local descriptor|TBA      |TBA|TBA|
|geolabel/mask.bin        |Image retrieval |TBA      |TBA|TBA|
|geolabel/overlap_rank.txt|Image retrieval |TBA      |TBA|TBA|

The mesh reconstruction is available for preview by substituting `<pid>` in the following link:

```
https://www.altizure.com/project-model?pid=<pid>
```

An example is provided [here](https://www.altizure.com/project-model?pid=57f8d9bbe73f6760f10e916a).

[1]: https://arxiv.org/abs/1811.10343