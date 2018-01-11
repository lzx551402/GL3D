# GL3D: Geometric Learning with 3D Reconstruction

The `GL3D` is a large-scale database consisting of various types of scene data for geometry-related learning problems.
This repo also contains a toolbox which implements the evaluation protocol for matchable image retrieval task as introduced in the relevant `CVPR 2017` publication [[1]](#refs).

## Dataset Description

The `GL3D` contains 90,590 high-resolution images in 378 different scenes. 
Each scene contains 50 to 1,000 images with large geometric overlaps, covering urban, rural area, or scenic spots captured by drones from multiple scales and perspectives. Several small objects are also included to enrich the data diversity.

Each scene data is reconstructed to generate a triangular mesh model by the state-of-the-art 3D reconstruction pipeline.
A quick view of the GL3D is given below.

![Example sequence](img/dataset_view.png)

For each scene data, we provide the complete image sequence, geometric labels.