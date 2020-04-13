## visualize.py

An example tool for visualizing geometric labels or reconstruction results.

Visualize image keypoints.
```
python visualize.py kpt
```
![Visualization keypoints](../imgs/example_kpt.png)

Visualize matching results.
```
python visualize.py match
```
![Visualiztion matches](../imgs/example_match.png)

Visualize overlap masks.
```
python visualize.py mask
```
![Visualiztion masks](../imgs/example_mask.png)

Visualize corresponding patches.
```
python visualize.py patch
```
![Visualiztion corresponding patches](../imgs/example_patch.png)

Visualize depth maps.
```
python visualize.py depth
```
![Visualizeation depths](../imgs/example_depth.png)

To visualize blended images or rendered depths, pass ``--blended`` when running above scripts.