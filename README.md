# GL3D: Geometric Learning with 3D Reconstruction
![Example sequence](imgs/gl3d_view.png)

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

GL3D is now tighly combined with [BlendedMVS](https://github.com/YoYo000/BlendedMVS), referred to as BlendedMVG. If you have used the rendered depths or blended images, please also cite:

    @inproceedings{yao2020blendedmvs,
      title={BlendedMVS: A Large-scale Dataset for Generalized Multi-view Stereo Networks},
      author={Yao, Yao and Luo, Zixin and Li, Shiwei and Zhang, Jingyang and Ren, Yufan and Zhou, Lei and Fang, Tian and Quan, Long},
      booktitle={Computer Vision and Pattern Recognition (CVPR)},
      year={2020}
    }

## Dataset Description

GL3D contains 125,623 high-resolution images regarding 543 different scenes. 
Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline. 
Refer to [\[1\]][1] for details. 
For each scene data, we provide the complete image sequence, geometric labels and reconstruction results.

To increase the data diversity, we have also applied the same data generation pipeline on some Internet tourism datasets that are publicly available.
In practice, we recommend using both GL3D and tourism datasets collaboratively in training for better generalization ability.
Refer to [docs/tourism_data.md](docs/tourism_data.md) for details.

## Tasks

Research works below are supported by GL3D:

|Task            |Reference                                           |
|:--------------:|:--------------------------------------------------:|
|Image retrieval |[MIRorR](https://arxiv.org/abs/1811.10343), ACCV'18 |
|Local descriptor|[GeoDesc](https://arxiv.org/abs/1807.06294), ECCV'18|
|Local descriptor|[ContextDesc](https://arxiv.org/abs/1904.04084), CVPR'19|
|Outlier rejection|[OANet](https://arxiv.org/abs/1908.04964), ICCV'19|
|Local feature   |[ASLFeat](https://arxiv.org/abs/2003.10071), CVPR'20|

## Downloads

Undistorted images resized to 1000x1000 are provided.

| Sources |    Data Name   |Link|Disk|       Descriptions       |
|:-------:|:--------------:|:--:|:--:|:------------------------:|
|   GL3D  |    gl3d_imgs   |[URL](https://1drv.ms/u/s!Anl8gFgW1C7LknxGy1gesj30SQ1I?e=RTT6re)|62G |1000x1000 undistorted images of GL3D |
|   GL3D  | gl3d_raw_imgs  |[URL](https://1drv.ms/u/s!Anl8gFgW1C7Lknv-RWaTA_OzkZjI?e=HtbfYU)|52G |raw images of test set of GL3D       |
|   GL3D & BlendedMVS | gl3d_blended_images |[URL](https://1drv.ms/u/s!Anl8gFgW1C7LknrD6mmoVC7f7HYH?e=8CeQeb)|58G |1000x1000 blended images of GL3D and BlendedMVS |


## Dataset Format 

```
data                          
 └── <pid> 
       ├── undist_images/*
       ├── blended_images/*
       ├── geolabel/*
       ├── img_kpts/*.bin
       ├── depths/*.pfm
       ├── rendered_depths/*.pfm
       └── image_list.txt
```

|File Name                |Data Name  |Link|Disk |Task            |Descriptions                                                         |
|:------------------------|:---------:|:--:|:---:|:--------------:|:-------------------------------------------------------------------:|
|geolabel/cameras.txt          |gl3d_cams           |[URL](https://1drv.ms/u/s!Anl8gFgW1C7Lkmf-zEcSRRlGPQyv?e=2nFWxn)|<0.1G|Common          |Camera intrisic/extrinsic parameters, recovered by SfM.|
|img_kpts/<img_idx>.bin        |gl3d_kpts           |[URL](https://1drv.ms/u/s!Anl8gFgW1C7Lknh620XvMjxW8yrs?e=ZwLmye)|28G  |Common          |Image keypoints detected by SIFT.                      |
|depths/<img_idx>.pfm          |gl3d_depths         |[URL](https://1drv.ms/u/s!Anl8gFgW1C7Lknn3rHDqrg_7OMwt?e=pWsbs7)|30G  |Common          |Depth maps from MVS algorithms.                        |
|rendered_depths/<img_idx>.pfm |gl3d_rendered_depths|[URL](https://1drv.ms/u/s!Anl8gFgW1C7LknerrzkrkiOae4JN?e=mHVhg3)|30G  |Common          |Depth maps rendered from 3D mesh models                |
|geolabel/corr.bin        |gl3d_corr  |[URL](https://1drv.ms/u/s!Anl8gFgW1C7LkmhoY66o5bViFhZ-?e=ZOXRXV)|6.1G |Local descriptor|Image correspondences that haved survived from SfM.                  |
|geolabel/mask.bin        |gl3d_mask  |[URL](https://1drv.ms/u/s!Anl8gFgW1C7Lknbi0W0A30i7BMTO?e=1N1QWC)|5.3G |Image retrieval |Overlap masks of image pairs, computed from mesh re-projections.     |
|geolabel/common_track.txt|gl3d_ct    |[URL](https://1drv.ms/u/s!Anl8gFgW1C7LkmXVtj6a72czehJU?e=NhfuzD)|<0.1G|Image retrieval |Common track ratio of image pairs, computed from SfM.                |
|geolabel/mesh_overlap.txt|gl3d_mo    |[URL](https://1drv.ms/u/s!Anl8gFgW1C7LkmYojA4pxN4FYXgn?e=cDM4d8)|<0.1G|Image retrieval |Mesh overlap ratio of image pairs, computed from mesh re-projections.|

For data organization, refer to [docs/data_format.md](docs/data_format.md).

Python-based IO utilities are provided to parse the data, refer to [utils/io.py](utils/io.py).

Visualizations and examples of usage can be found in [example/README.md](example/README.md).

Please feel free to inform us if you need some other intermediate results for your research.

## Data Preview (not available anymore)
The mesh reconstruction is available for preview by substituting `<pid>` in the following link:

```
https://www.altizure.com/project-model?pid=<pid>
```

~~An example is provided [here](https://www.altizure.com/project-model?pid=57f8d9bbe73f6760f10e916a).~~
~~Noted that some projects are not online available, from `000000000000000000000000` to `00000000000000000000001d`.~~

## Acknowledgments
This dataset is prepared and maintained by
[Zixin Luo](mailto:zluoag@cse.ust.hk),
[Tianwei Shen](mailto:tshenaa@cse.ust.hk),
[Jacky Tang](mailto:jackytck@gmail.com) and
[Tian Fang](mailto:fangtian@altizure.com).
3D reconstructions are obtained by [Altizure](https://www.altizure.com/).

We also thank [Yao Yao](mailto:yyaoag@cse.ust.hk) and [Lei Zhou](mailto:lzhouai@cse.ust.hk) for generating rendered depths and blended images to further improve the data quality.

[1]: https://arxiv.org/abs/1811.10343

## Changelog
### 2019-9-17 Releasing of GL3D_V2
- Another 165 datasets are added, covering mainly landmarks and small objects.
- Rerun SfM for all datasets with [GeoDesc](https://github.com/lzx551402/geodesc) to obtain denser reconstruction.
- Camera distortion parameters are provided.
- Undistorted images are provided.
- More helper functions to perform geometry computation.

### 2019-12-4 Update GL3D_V2
- Provide depth maps to enrich geometric labels.
- Provide helper functions to parse depth maps.

### 2019-12-16 Update GL3D_V2
- Another 530 Internet tourism datasets are added to enrich the data.
- Mesh overlapping ratio and overlapping masks are provided.

### 2020-4-13 Update GL3D_V2
- Add download link to rendered depths and blended images, and further refer to the combination of GL3D and BlendedMVS as BlendedMVG, for solving general multi-view geometry problems. Please visit [BlendedMVS](https://github.com/YoYo000/BlendedMVS) and refer to its respective [paper](https://arxiv.org/abs/1911.10127) for details.

### 2023-04-12 Update GL3D_V2
- Update download links.
