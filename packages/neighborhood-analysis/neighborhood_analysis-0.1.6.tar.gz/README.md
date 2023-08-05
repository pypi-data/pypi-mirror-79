# Neighborhood analysis

![Build](https://github.com/Mr-Milk/neighborhood_analysis/workflows/Build/badge.svg) ![pypi](https://badgen.net/pypi/v/neighborhood_analysis)

A python version of neighborhood analysis, purposed in [histocat](https://www.nature.com/articles/nmeth.4391). The analysis is 
to profile cell-cell interaction.

The safe parallelism has been implemented, so no need to do multiprocessing yourself.

(This is my first rust project, suggestions are welcomed.)

## Installation

The wheels are built for Windows, MacOS, Linux in 64bit, and Python version 3.5, 3.6, 3.7, 3.8

Requirements: Python >= 3.5

### From pypi

Normally, there should be a compatible wheel for your system. Just run:

```shell script
pip install neighborhood_analysis
```

If not, it will try to compile from source, you need to install dependencies.

```shell script
# for windows
choco install rustup.install
# for Unix
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

pip install maturin

pip install neighborhood_analysis
```


### From source

Assume you have all the above dependencies, clone the repo, and then run:

```shell script
pip install .
```

## Usage

```python
import numpy as np
from neighborhood_analysis import CellCombs, get_point_neighbors, comb_bootstrap

# Get 10000 points, represent cell location
points = np.random.randint(0, 1000, (10000, 2))

# Assign each cell with a type
types_pool = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
types = np.random.choice(types_pool, 10000)

# Find cell neighbors at radius set at 10
# The points must be a list of tuple, otherwise it will raise TypeError
points = [(x, y) for (x, y) in points]
neighbors = get_point_neighbors(points, 10.0)

cc = CellCombs(types)
result = cc.bootstrap(types, neighbors)
# On my dual-core mac, this step takes 6~7 seconds.

X = [bool(i) for i in np.random.choice([True, False], 10000)]
Y = [bool(i) for i in np.random.choice([True, False], 10000)]
# The types must be a list of bool
z_score = comb_bootstrap(X, Y, neighbors, ignore_self=True)

```

## Documentation

```python

def get_bbox(points_collections):
    """A utility function to return minimum bounding box list of polygons
    
        Args:
            points_collections: List[List[(float, float)]]; List of 2d points collections
        
        Return:
            A dictionary of the index of every points, with the index of its neighbors

    """

def get_point_neighbors(points, r):
    """A utility function to search for neighbors
    
        Args:
            points: List[tuple(float, float)]; Two dimension points
            r: float; The search radius
    
        Return:
            A dictionary of the index of every points, with the index of its neighbors

    """


def get_bbox_neighbors(bbox, expand=0.0, scale=1.0):
    """A utility function to search for bbox neighbors using r-tree
    
        Args:
            bbox_list: List[tuple(float, float, float, float)]; 
                The minimum bounding box of any polygon (minx, miny, maxx, maxy)
            expand: float; The expand unit
            scale: float; The scale fold number
        
        Return:
            A dictionary of the index of every rect, with the index of its neighbors
    
    """


def comb_bootstrap(x_status, y_status, neighbors, times=500, ignore_self=False):
    """Bootstrap between two types

        If you want to test co-localization between protein X and Y, first determine if the cell is X-positive
        and/or Y-positive. True is considered as positive and will be counted.
    
        Args:
            x_status: List[bool]; If cell is type x
            y_status: List[bool]; If cell is type y
            neighbors: Dict[int, List[int]]; eg. {1:[4,5], 2:[6,7]}, cell at index 1 has neighbor cells from index 4 and 5
            times: int (500); How many times to perform bootstrap
            ignore_self: bool (False); Whether to consider self as a neighbor
        
        Return:
            The z-score for the spatial relationship between X and Y

    """


class CellCombs:

    def __init__(self, types, order=False):
        """Constructor function
        
            Args:
             types: List[str]; All the type of cells in your research
             order: bool (False); If False, the ('A', 'B') and ('A', 'B') is the same.
            
            Return:
             self

        """
    
    def bootstrap(self, types, neighbors, times=500, pval=0.05, method="pval", ignore_self=False):
        """Bootstrap functions
        
            If method is 'pval', 1.0 means association, -1.0 means avoidance.
            If method is 'zscore', results is the exact z-score value.
            
            Args:
                types: List[str]; The type of all the cells
                neighbors: Dict[int, List[int]]; eg. {1:[4,5], 2:[6,7]}, cell at index 1 has neighbor cells from index 4 and 5
                times: int (500); How many times to perform bootstrap
                pval: float (0.05); The threshold of p-value
                method: str ('pval'); 'pval' or 'zscore'
                ignore_self: bool (False); Whether to consider self as a neighbor
            
            Return:
                List of tuples, eg.(['a', 'b'], 1.0), the type a and type b has a relationship as association
        
        """

```
