# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import namedtuple
from dataclasses import dataclass

import h5py as h5
import numpy as np

__all__ = ["create_minimal_h5_file"]


@dataclass
class _ElementCoordinateSystem:
    """Element coordinate system definition.

    Attributes
    ----------
    normal : list[float]
        Normal vector of the element coordinate system.
    one_direction : list[float]
        Primary direction vector of the element coordinate system.
    """

    normal: list[float]
    one_direction: list[float]


@dataclass
class _MeshInfo:
    """Mesh information container.

    Attributes
    ----------
    element_set : any
        The element set dataset.
    n_elements : any
        Number of elements in the mesh.
    """

    element_set: any
    n_elements: any


def _get_element_nodes(element):
    """Calculate node coordinates for a quadrilateral element.

    Parameters
    ----------
    element : namedtuple
        Element with 'center' and 'edge_length' attributes, and optionally
        'element_coordinate_system' attribute containing normal and one_direction.

    Returns
    -------
    np.ndarray
        Array of shape (4, 3) containing the coordinates of the four corner nodes.
    """
    distance_from_center = element.edge_length / 2.0
    center = np.array(element.center)
    if hasattr(element, "element_coordinate_system"):
        normal = element.element_coordinate_system.normal
        one_direction = element.element_coordinate_system.one_direction
    else:
        normal = np.array([0.0, 0.0, 1.0])
        one_direction = np.array([1.0, 0.0, 0.0])

    two_direction = np.cross(normal, one_direction)

    return np.array(
        [
            center - distance_from_center * (one_direction + two_direction),
            center + distance_from_center * (one_direction - two_direction),
            center + distance_from_center * (one_direction + two_direction),
            center + distance_from_center * (two_direction - one_direction),
        ]
    )


def _create_mesh_data_set_with_single_element_set(root, elements, mesh_name="mesh0"):
    """Create a mesh dataset with a single element set in the HDF5 file.

    Creates mesh data including element labels, element nodes, element types,
    node labels, node coordinates, and an element set containing all elements.

    Parameters
    ----------
    root : h5py.Group
        Root group in the HDF5 file where the mesh will be created.
    elements : list
        List of element objects, each with 'center' and 'edge_length' attributes.
    mesh_name : str, optional
        Name for the mesh group. Default is "mesh0".

    Returns
    -------
    _MeshInfo
        Named tuple containing the element_set and n_elements.
    """
    meshes = root.create_group("meshes")

    nodes_per_element = 4
    quad_element_type = 4

    n_elements = len(elements)
    element_range = range(n_elements)

    mesh = meshes.create_group(mesh_name)
    mesh.create_dataset("element_labels", data=element_range)
    element_nodes = mesh.create_dataset(
        "element_nodes", (n_elements,), dtype=h5.vlen_dtype(np.dtype("int32"))
    )
    for i in element_range:
        start = i * nodes_per_element
        end = (i + 1) * nodes_per_element
        element_nodes[i] = range(start, end)

    mesh.create_dataset("element_types", data=np.ones(n_elements) * quad_element_type)
    mesh.create_dataset("node_labels", data=range(n_elements * nodes_per_element))

    nodes = []
    for element in elements:
        nodes.extend(_get_element_nodes(element))

    mesh.create_dataset("nodes", data=nodes)
    element_sets = mesh.create_group("element_sets")
    element_set_name = "element_set0"
    element_set = element_sets.create_dataset(element_set_name, data=element_range)

    return _MeshInfo(element_set=element_set, n_elements=n_elements)


def _create_single_component_linked_to_element_set(
    root, element_set_path, data_map_path, ply_angle=0.0
):
    """Create a component linked to an element set and data map.

    Creates a component group with soft links to the specified element set
    and data map, and sets the ply orientation angle.

    Parameters
    ----------
    root : h5py.Group
        Root group in the HDF5 file where the component will be created.
    element_set_path : str
        HDF5 path to the element set to link to.
    data_map_path : str
        HDF5 path to the data map to link to.
    ply_angle : float, optional
        Ply orientation angle in degrees. Default is 0.0.

    Returns
    -------
    h5py.Group
        The created component group.
    """
    components = root.create_group("components")
    component = components.create_group("component0")
    component["element_set"] = h5.SoftLink(element_set_path)
    component["data_map"] = h5.SoftLink(data_map_path)
    component.attrs["orientation"] = ply_angle
    return component


def _create_single_data_map_linked_to_element_set(root, element_set_path):
    """Create a data map linked to an element set.

    Creates a data map group with a soft link to the specified element set.

    Parameters
    ----------
    root : h5py.Group
        Root group in the HDF5 file where the data map will be created.
    element_set_path : str
        HDF5 path to the element set to link to.

    Returns
    -------
    h5py.Group
        The created data map group.
    """
    data_maps = root.create_group("data_maps")
    data_map = data_maps.create_group("data_map0")
    data_map["element_set"] = h5.SoftLink(element_set_path)
    return data_map


def _create_single_rosette(root, coordinate_system=None):
    """Create a rosette with a coordinate system definition.

    Creates a rosette group containing a coordinate system dataset.

    Parameters
    ----------
    root : h5py.Group
        Root group in the HDF5 file where the rosette will be created.
    coordinate_system : list of list of float, optional
        Coordinate system definition as a 4x3 array representing origin and
        three axis directions. Default is identity at origin [[0,0,0], [1,0,0], [0,1,0], [0,0,1]].

    Returns
    -------
    h5py.Group
        The created rosette group.
    """
    if coordinate_system is None:
        coordinate_system = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    rosettes = root.create_group("rosettes")
    rosette = rosettes.create_group("rosette")
    rosette.create_dataset("coord_sys", data=coordinate_system)
    return rosette


def _get_fixed_size_string(string):
    """Convert a string to a fixed-size NumPy string array.

    ACP fails to read variable length strings. This is a workaround to create
    fixed size strings which are correctly supported by ACP.

    Parameters
    ----------
    string : str
        The string to convert.

    Returns
    -------
    np.ndarray
        Fixed-size string array compatible with ACP.
    """
    return np.array(string, dtype="S" + str(len(string)))


def _create_material(fabrics, thickness=0.1):
    """Create a material (fabric) with default structural steel properties.

    Creates a fabric group with cost and mechanical property attributes,
    including elastic moduli, shear moduli, Poisson's ratios, thermal
    expansion coefficients, and other material parameters.

    Parameters
    ----------
    fabrics : h5py.Group
        Fabrics group where the material will be created.
    thickness : float, optional
        Cured thickness of the material. Default is 0.1.

    Returns
    -------
    h5py.Group
        The created fabric group.
    """
    fabric = fabrics.create_group("fabric1")
    fabric.attrs["TITLE"] = _get_fixed_size_string("Structural Steel")

    cost = fabric.create_group("cost")
    cost.attrs["cost_per_area"] = 0.0
    cost.attrs["currency"] = _get_fixed_size_string("USD")

    mechanical = fabric.create_group("mechanical")
    mechanical.attrs["E1"] = 1e6
    mechanical.attrs["E2"] = 1e6
    mechanical.attrs["E3"] = 1e6
    mechanical.attrs["G12"] = 1e6
    mechanical.attrs["G23"] = 1e6
    mechanical.attrs["G31"] = 1e6
    mechanical.attrs["alpha1"] = 1e-6
    mechanical.attrs["alpha2"] = 1e-6
    mechanical.attrs["alpha3"] = 1e-6
    mechanical.attrs["alpha_ref_temp"] = 20.0
    mechanical.attrs["architecture"] = _get_fixed_size_string("woven")
    mechanical.attrs["cured_thickness"] = thickness
    mechanical.attrs["v12"] = 0.04
    mechanical.attrs["v13"] = 0.3
    mechanical.attrs["v23"] = 0.3
    mechanical.attrs["weight_per_area"] = 10
    return fabric


def create_minimal_h5_file(file_path: str):
    """Creates a minimal HDF5 composite CAE file.


    Parameters
    ----------
    file_path:
        Path where the file is created.
    """
    with h5.File(file_path, "w") as f:
        root = f.create_group("composite_cae")
        Element = namedtuple("Element", ["center", "edge_length"])
        # Use large edge length so always something gets mapped (also if units are micro-meters)
        element = Element(center=[0.0, 0.0, 0.0], edge_length=1000)
        mesh_info = _create_mesh_data_set_with_single_element_set(
            root, elements=[element]
        )
        data_map = _create_single_data_map_linked_to_element_set(
            root, mesh_info.element_set.name
        )
        data_map.create_dataset(
            "reference_directions",
            data=np.tile([1.0, 0.0, 0.0], (mesh_info.n_elements, 1)),
        )
        data_map.create_dataset(
            "matorient_1_angles", data=np.zeros(mesh_info.n_elements, dtype="float")
        )
        component = _create_single_component_linked_to_element_set(
            root, mesh_info.element_set.name, data_map.name
        )
        material_data = root.create_group("material_data")
        fabrics = material_data.create_group("fabrics")
        fabric1 = _create_material(fabrics)

        component["material"] = h5.SoftLink(fabric1.name)
