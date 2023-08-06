<!-- <div align="center">
  <img src="https://raw.githubusercontent.com/leomariga/pyTruthTable/master/doc/logo.png"><br>
</div> -->

<!-- -----------------
[![PyPI Latest Release](https://img.shields.io/pypi/v/pyTruthTable.svg?style=for-the-badge)](https://pypi.org/project/pyTruthTable/)
[![License](https://img.shields.io/pypi/l/pyTruthTable.svg?style=for-the-badge)](https://github.com/leomariga/pyTruthTable/blob/master/LICENSE)
 -->
## What is pyRANSAC-3D?
**_pyRANSAC-3D_** is an open source implementation of  .

#### Features:
 - Cylinder
 - Plane
 - Cuboid


## Installation
Requirements: Nympy

Install with [Pypi](https://pypi.org/project/pyransac3d/):

```sh
pip3 install pyransac3d
```

### Take a look: 

##### Example 1 - Binary operations

``` python
import pyransac3d as pyrsc

points = load_points(.)

plano1 = pyrsc.Plane()
best_eq, best_inliers = plano1.fit(points, 0.01)

```

Results in the plane equation Ax+By+Cz+D:
`[1, 0.5, 2, 0]`


## Documentation & other links
 - The [amazing documentation is this Ṕage](https://leomariga.github.io/pyRANSAC-3D/).
 - Source code in the [Github repository](https://github.com/leomariga/pyRANSAC-3D).
 - [Pypi pakage installer](https://pypi.org/project/pyransac3d/)


## License
[MIT](https://github.com/leomariga/pyRANSAC-3D/blob/master/LICENSE)

## Contributing is awesome!

See [CONTRIBUTING](https://github.com/leomariga/pyRANSAC-3D/blob/master/CONTRIBUTING.md)




## Contact

Developed with :heart: by [Leonardo Mariga](https://github.com/leomariga) 

leomariga@gmail.com

Did you like it? Remember to click on :star2: button.
