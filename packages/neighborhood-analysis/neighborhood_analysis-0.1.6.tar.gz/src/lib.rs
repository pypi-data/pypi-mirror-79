mod utils;
use utils::*;

use rand::thread_rng;
use rand::seq::SliceRandom;
use itertools::Itertools;
use kdbush::KDBush;
use rstar::{RTree, RTreeObject, AABB};
use spade::{BoundingRect};
use std::collections::HashMap;
use counter::Counter;
use rayon::prelude::*;

// pyo3 dependencies
use pyo3::prelude::*;
use pyo3::exceptions::ValueError as PyValueError;
use pyo3::wrap_pyfunction;

#[pymodule]
fn neighborhood_analysis(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<CellCombs>()?;
    m.add_wrapped(wrap_pyfunction!(get_bbox))?;
    m.add_wrapped(wrap_pyfunction!(get_point_neighbors))?;
    m.add_wrapped(wrap_pyfunction!(get_bbox_neighbors))?;
    m.add_wrapped(wrap_pyfunction!(comb_bootstrap))?;
    Ok(())
}


/// A utility function to return minimum bounding box list of polygons
///
/// Args:
///     points_collections: List[List[(float, float)]]; List of 2d points collections
///
/// Return:
///     A dictionary of the index of every points, with the index of its neighbors
///
#[pyfunction]
fn get_bbox(points_collections: Vec<Vec<(f64, f64)>>)
-> Vec<(f64, f64, f64, f64)> {

    let bbox: Vec<(f64, f64, f64, f64)> = points_collections.par_iter().map(|p| {
        let points: Vec<[f64;2]> = p.iter().map(|ps| [ps.0, ps.1]).collect();
        let rect = BoundingRect::from_points(points);
        let lower: [f64;2] = rect.lower();
        let upper: [f64;2] = rect.upper();
        (lower[0], lower[1], upper[0], upper[1])
    }).collect();

    bbox
}


/// A utility function to search for point neighbors using kd-tree
///
/// Args:
///     points: List[tuple(float, float)]; Two dimension points
///     r: float; The search radius
///
/// Return:
///     A dictionary of the index of every points, with the index of its neighbors
///
#[pyfunction]
fn get_point_neighbors(points: Vec<(f64, f64)>, r: f64)
    -> HashMap<usize, Vec<usize>>{
    let tree = KDBush::create(points.to_owned(), kdbush::DEFAULT_NODE_SIZE); // make an index
    let result: HashMap<usize, Vec<usize>> = points.par_iter().enumerate().map(|(i ,p)| {
        let mut neighbors:Vec<usize> = vec![];
        tree.within(p.0, p.1, r, |id| neighbors.push(id));
        (i, neighbors)
    }).collect();

    result
}

// customize object to insert in to R-tree
struct Rect
{
    minx: f64,
    miny: f64,
    maxx: f64,
    maxy: f64,
    index: usize,
}

impl Rect {
    fn new(bbox:(f64, f64, f64, f64), index: usize) -> Rect {
        Rect{
            minx: bbox.0,
            miny: bbox.1,
            maxx: bbox.2,
            maxy: bbox.3,
            index
        }
    }
}

impl RTreeObject for Rect
{
    type Envelope = AABB<[f64; 2]>;

    fn envelope(&self) -> Self::Envelope
    {
        AABB::from_corners([self.minx, self.miny], [self.maxx, self.maxy])
    }
}

/// A utility function to search for bbox neighbors using r-tree
///
/// Args:
///     bbox_list: List[tuple(float, float, float, float)]; The minimum bounding box of any polygon
///             (minx, miny, maxx, maxy)
///     expand: float; The expand unit
///     scale: float; The scale fold number
///
/// Return:
///     A dictionary of the index of every rect, with the index of its neighbors
///
#[pyfunction]
fn get_bbox_neighbors(bbox_list: Vec<(f64, f64, f64, f64)>, expand: Option<f64>, scale: Option<f64>)
-> HashMap<usize, Vec<usize>> {
    let mut expand_na: bool = true;
    let expand: f64 = match expand {
            Some(data) => {
                expand_na = false;
                data
            },
            None => 0.0
        };

    let scale: f64 = match scale {
            Some(data) => data,
            None => 1.0
        };


    let aabb: Vec<Rect> = bbox_list.par_iter().enumerate().map(|(i, b)|
        {
            Rect::new(b.to_owned(), i)
        }
    ).collect();
    let tree: RTree<Rect> = RTree::<Rect>::bulk_load(aabb);
    let search_aabb: Vec<Rect> = {
        if expand_na == false {
            let expand_aabb: Vec<Rect> = bbox_list.par_iter().enumerate().map(|(i, b)|
                {
                    Rect::new((b.0 - expand, b.1 - expand, b.2 + expand, b.3 + expand), i)
                }
            ).collect();
            expand_aabb
        } else {
            let scale_aabb: Vec<Rect> = bbox_list.par_iter().enumerate().map(|(i, b)|
                {
                    let xexpand: f64 = (b.2 - b.0) * (scale - 1.0);
                    let yexpand: f64 = (b.3 - b.1) * (scale - 1.0);
                    Rect::new((b.0 - xexpand, b.1 - yexpand, b.2 + xexpand, b.3 + yexpand), i)
                }
            ).collect();
            scale_aabb
        }};
    let result: HashMap<usize, Vec<usize>> = search_aabb.par_iter().map(|rect| {
        let envelop = rect.envelope();
        let search_result: Vec<&Rect> = tree.locate_in_envelope_intersecting(&envelop).collect();
        let neighbors: Vec<usize> = search_result.iter().map(|r| r.index).collect();
        (rect.index, neighbors)
    }).collect();

    result

}

/// Bootstrap between two types
///
/// If you want to test co-localization between protein X and Y, first determine if the cell is X-positive
/// and/or Y-positive. True is considered as positive and will be counted.
///
/// Args:
///     x_status: List[bool]; If cell is type x
///     y_status: List[bool]; If cell is type y
///     neighbors: Dict[int, List[int]]; eg. {1:[4,5], 2:[6,7]}, cell at index 1 has neighbor cells from index 4 and 5
///     times: int (500); How many times to perform bootstrap
///     ignore_self: bool (False); Whether to consider self as a neighbor
///
/// Return:
///     The z-score for the spatial relationship between X and Y
///
#[pyfunction]
fn comb_bootstrap(
    py: Python,
    x_status: PyObject,
    y_status: PyObject,
    neighbors: PyObject,
    times: Option<usize>,
    ignore_self: Option<bool>,
) -> PyResult<f64> {

    let x: Vec<bool> = match x_status.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `x_status`, should be list of bool."))
            }
        };

    let y: Vec<bool> = match y_status.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `y_status`, should be list of bool."))
            }
        };

    let neighbors_data: HashMap<usize, Vec<usize>> = match neighbors.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `neighbors`, should be a dict."))
            }
        };

    let times = match times {
            Some(data) => data,
            None => 500
        };

    let ignore_self = match ignore_self {
            Some(data) => data,
            None => false
        };

    let real: f64 = comb_count_neighbors(&x, &y, &neighbors_data, ignore_self) as f64;

    let perm_counts: Vec<usize> = (0..times).into_par_iter().map(|_| {
        let mut rng = thread_rng();
        let mut shuffle_y = y.to_owned();
        shuffle_y.shuffle(&mut rng);
        let perm_result = comb_count_neighbors(
            &x,
            &shuffle_y,
            &neighbors_data,
            ignore_self);
        perm_result
        })
        .collect();

    let m = mean(&perm_counts);
    let sd = std(&perm_counts);

    Ok((real - m) / sd)
}

/// Constructor function
///
/// Args:
///     types: List[str]; All the type of cells in your research
///     order: bool (False); If False, the ('A', 'B') and ('A', 'B') is the same.
///
/// Return:
///     self
///
#[pyclass]
struct CellCombs {
    #[pyo3(get)]
    cell_types: PyObject,
    #[pyo3(get)]
    cell_combs: PyObject,
    #[pyo3(get)]
    cell_relationships: PyObject,
}

unsafe impl Send for CellCombs {}

#[pymethods]
impl CellCombs {
    #[new]
    fn new(py:Python, types: PyObject, order: Option<bool>) -> PyResult<Self> {

        let types_data: Vec<&str> = match types.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `types`, should be list of string."))
            }
        };

        let order_data: bool = match order {
            Some(data) => data,
            None => false,
        };

        let uni: Vec<&str> = types_data.into_iter().unique().collect();
        let mut combs = vec![];
        let mut relationships = HashMap::new();

        for i1 in uni.to_owned() {
            relationships.insert(i1, vec![]);
            for i2 in uni.to_owned() {
                if order_data {
                    combs.push(vec![i1, i2]);
                }
                relationships.get_mut(i1).unwrap().push(vec![i1, i2]);
            }
        }

        if !order_data {
            let end: usize = uni.len();
            for (i, e) in uni.to_owned().iter().enumerate() {
                for t in i..end {
                    combs.push(vec![e, uni[t]]);
                }
            }
        }

        let uni_py = uni.to_object(py);
        let combs_py = combs.to_object(py);
        let relationships_py = relationships.to_object(py);

        Ok(CellCombs {
            cell_types: uni_py,
            cell_combs: combs_py,
            cell_relationships: relationships_py,
        })
    }

    /// Bootstrap functions
    ///
    /// If method is 'pval', 1.0 means association, -1.0 means avoidance.
    /// If method is 'zscore', results is the exact z-score value.
    ///
    /// Args:
    ///     types: List[str]; The type of all the cells
    ///     neighbors: Dict[int, List[int]]; eg. {1:[4,5], 2:[6,7]}, cell at index 1 has neighbor cells from index 4 and 5
    ///     times: int (500); How many times to perform bootstrap
    ///     pval: float (0.05); The threshold of p-value
    ///     method: str ('pval'); 'pval' or 'zscore'
    ///     ignore_self: bool (False); Whether to consider self as a neighbor
    ///
    /// Return:
    ///     List of tuples, eg.(['a', 'b'], 1.0), the type a and type b has a relationship as association
    ///
    fn bootstrap(&self,
                 py: Python,
                 types: PyObject,
                 neighbors: PyObject,
                 times: Option<usize>,
                 pval: Option<f64>,
                 method: Option<&str>,
                 ignore_self: Option<bool>,
    ) -> PyResult<PyObject> {

        let types_data: Vec<&str> = match types.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `types`, should be list of string."))
            }
        };
        let neighbors_data: HashMap<usize, Vec<usize>> = match neighbors.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Can't resolve `neighbors`, should be a dict."))
            }
        };

        let times = match times {
            Some(data) => data,
            None => 500
        };

        let pval = match pval {
            Some(data) => data,
            None => 0.05
        };

        let method = match method {
            Some(data) => data,
            None => "pval"
        };

        let ignore_self = match ignore_self {
            Some(data) => data,
            None => false
        };

        let cellcombs: Vec<Vec<&str>> = match self.cell_combs.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Resolve cell_combs failed."))
            }
        };
        let cellrelatetionship: HashMap<&str, Vec<Vec<&str>>> = match self.cell_relationships.extract(py) {
            Ok(data) => data,
            Err(_) => {
                return Err(PyValueError::py_err("Resolve cell_relationship failed."))
            }
        };

        let real_data = count_neighbors(
            &types_data,
            &neighbors_data,
            &cellcombs,
            &cellrelatetionship,
            ignore_self
        );

        let mut simulate_data = cellcombs.iter()
            .map(|comb| (comb.to_owned(), vec![]))
            .collect::<HashMap<Vec<&str>, Vec<f64>>>();

        let all_data: Vec<HashMap<Vec<&str>, f64>> = (0..times).into_par_iter().map(|_| {
            let mut rng = thread_rng();
            let mut shuffle_types = types_data.to_owned();
            shuffle_types.shuffle(&mut rng);
            let perm_result = count_neighbors(
                &shuffle_types,
                &neighbors_data,
            &cellcombs,
            &cellrelatetionship,
            ignore_self);
            perm_result
            })
            .collect();

        for perm_result in all_data {
            for (k, v) in perm_result.iter() {
                simulate_data.get_mut(k).unwrap().push(*v);
        }
        };
/*
        let mut results = cellcombs.iter()
            .map(|comb| (comb.to_owned(), 0.0))
            .collect::<HashMap<Vec<&str>, f64>>();*/
        let mut results: Vec<(Vec<&str>, f64)> = vec![];

        for (k, v) in simulate_data.iter() {
            let real = real_data[k];

            if method == "pval" {
                let mut gt: f64 = 0.0;
                let mut lt: f64 = 0.0;
                for i in v.iter() {
                    if i >= &real {
                        gt += 1.0
                    }
                    if i <= &real {
                        lt += 1.0
                    }
                }
                let gt: f64 = gt as f64 / (times.to_owned() as f64 + 1.0);
                let lt: f64 = lt as f64 / (times.to_owned() as f64 + 1.0);
                let dir: f64 = (gt < lt) as i32 as f64;
                let udir: f64 = !(gt < lt) as i32 as f64;
                let p: f64 = gt * dir + lt * udir;
                let sig: f64 = (p < pval) as i32 as f64;
                let sigv: f64 = sig * (dir - 0.5).signum();
                // *results.get_mut(k).unwrap() += sigv;
                results.push((k.to_owned(), sigv));
            } else {
                let m = mean_f(v);
                let sd = std_f(v);
                if sd != 0.0 {
                    results.push((k.to_owned(), (real - m) / sd));
                    //*results.get_mut(k).unwrap() += (real - m) / sd;
                } else {
                    results.push((k.to_owned(), 0.0));
                    //*results.get_mut(k).unwrap() += 0.0;
                }

            }

        }

        let results_py = results.to_object(py);

        Ok(results_py)
    }
}

fn count_neighbors<'a>(
                   types: &Vec<&str>,
                   neighbors: &HashMap<usize, Vec<usize>>,
                   cell_combs: &Vec<Vec<&'a str>>,
                   cell_relationships: &HashMap<&'a str, Vec<Vec<&'a str>>>,
                   ignore_self: bool)
               -> HashMap<Vec<&'a str>, f64> {
    let mut storage = cell_combs.iter()
        .map(|comb| (comb.to_owned(), vec![]))
        .collect::<HashMap<Vec<&str>, Vec<usize>>>();

    for (k, v) in neighbors.iter() {
        let cent_type = types[*k];
        let neigh_type: Counter<_> = {
            if ignore_self {
                v.iter()
                    .filter_map(|i| if i != k { Some(types[*i]) } else { None })
                    .collect::<Counter<_>>()
            } else {
                v.iter()
                    .map(|i| types[*i])
                    .collect::<Counter<_>>()
            }
        };
        for comb in cell_relationships[cent_type].iter() {
            let counts = neigh_type.get(comb[1]).unwrap_or(&0);
            match storage.get_mut(comb) {
                None => {
                    storage.get_mut(&vec![comb[1], comb[0]]).unwrap().push(*counts)
                },
                Some(s) => s.push(*counts),
            };
        }
    }

    let mut results: HashMap<Vec<&'a str>, f64>= HashMap::new();
    for (k, v) in storage.iter() {
        results.insert(k.to_owned(), mean(&v));
    }

    results
}

fn comb_count_neighbors(
    x: &Vec<bool>,
    y: &Vec<bool>,
    neighbors: &HashMap<usize, Vec<usize>>,
    ignore_self: bool,
) -> usize {

    let mut count: usize = 0;

    for (k, v) in neighbors.iter() {
        if x[*k] {
            if ignore_self {
                for (i, c) in v.iter().enumerate() {
                    if i != *k {
                        if y[*c] { count += 1 }
                    }
                }
            } else {for c in v.iter() {
                    if y[*c] { count += 1 }
                }
            }
        }
    }

    count

}
