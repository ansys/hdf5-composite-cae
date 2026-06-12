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

import logging
from pathlib import Path

import h5py as h5

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__all__ = ["validate_file"]


class ErrorCollector:
    """Collects validation errors and manages error reporting.

    Attributes
    ----------
    _throw_on_first_error : bool
        If True, raises an exception immediately on first error.
    _errors : list[str]
        List of accumulated error messages.
    """

    def __init__(self, throw_on_first_error: bool):
        """Initialize the error collector.

        Parameters
        ----------
        throw_on_first_error : bool
            If True, raises an exception immediately on first error.
            If False, accumulates errors for later reporting.
        """
        self._throw_on_first_error = throw_on_first_error
        self._errors = []

    def checked_get(self, obj, key: str):
        """Get a key from an HDF5 object with error handling.

        Parameters
        ----------
        obj : h5py.Group or h5py.File
            The HDF5 object to get the key from.
        key : str
            The key to retrieve.

        Returns
        -------
        h5py.Group or h5py.Dataset or None
            The retrieved object, or None if an error occurred.
        """
        try:
            return obj[key]
        except Exception as e:
            err = f"Missing key '{key}' at {obj.name}"

            if self._throw_on_first_error:
                raise RuntimeError(err) from e
            log.error(err)
            self._errors.append(err)

    def raise_error(self, error):
        """Raise or collect an error.

        Parameters
        ----------
        error : str
            Error message to raise or collect.
        """
        if self._throw_on_first_error:
            raise RuntimeError(error)
        log.error(error)
        self._errors.append(error)

    def check_softlink(self, f, path: str):
        """Check if a path is a soft link.

        Parameters
        ----------
        f : h5py.File
            The HDF5 file object.
        path : str
            The path to check.
        """
        link = f.get(path, getlink=True)

        if not isinstance(link, h5.SoftLink):
            self.raise_error(f"{path} needs to be a softlink")

    def raise_accumlated_errors(self):
        """Raise accumulated errors if any exist."""
        if len(self._errors):
            raise RuntimeError("Validation errors:\n" + "\n".join(self._errors))


def _validate_components(f, components, error_collector, h5_file):
    """Validate components and their references.

    Parameters
    ----------
    f : h5py.File
        The HDF5 file object.
    components : h5py.Group
        Components group to validate.
    error_collector : ErrorCollector
        Error collector instance.
    h5_file : Path | str
        Path of the file being validated.
    """
    if components is None:
        return

    if len(components) == 0:
        error_collector.raise_error(f"No components in {h5_file}")

    for component in components.values():
        # nothing required
        material = error_collector.checked_get(component, "material")
        if material is not None:
            error_collector.check_softlink(f, material.name)
        element_set = error_collector.checked_get(component, "element_set")
        if element_set is not None:
            error_collector.check_softlink(f, element_set.name)
        data_map = error_collector.checked_get(component, "data_map")
        if data_map is not None:
            error_collector.check_softlink(f, data_map.name)


def _validate_material_data(material_data, error_collector, h5_file):
    """Validate material data and fabrics.

    Parameters
    ----------
    material_data : h5py.Group
        Material data group to validate.
    error_collector : ErrorCollector
        Error collector instance.
    h5_file : Path | str
        Path of the file being validated.
    """
    if material_data is None:
        return

    fabrics = error_collector.checked_get(material_data, "fabrics")
    if fabrics is not None and len(fabrics) == 0:
        error_collector.raise_error(f"No fabrics in {h5_file}")


def _validate_element_nodes(mesh, all_element_nodes, n_elements, error_collector):
    """Validate element nodes for a mesh.

    Parameters
    ----------
    mesh : h5py.Group
        Mesh group being validated.
    all_element_nodes : h5py.Dataset
        Element nodes dataset.
    n_elements : int
        Number of elements expected.
    error_collector : ErrorCollector
        Error collector instance.

    Returns
    -------
    int
        Maximum node index found.
    """
    if len(all_element_nodes) != n_elements:
        error_collector.raise_error(
            f"Mesh: {mesh.name}: Invalid number of element nodes in {mesh.name}. Expected {n_elements} but got {len(all_element_nodes)}"
        )

    if len(all_element_nodes.shape) == 2:
        _, num_columns = all_element_nodes.shape
        if num_columns == 1:
            all_element_nodes = all_element_nodes[:, 0]
        elif num_columns > 1:
            error_collector.raise_error(
                f"Mesh: {mesh.name}: element nodes has an invalid shape: {all_element_nodes.shape}. Should be ({n_elements}), ({n_elements}, ) or ({n_elements}, 1)"
            )

    max_node_index = 0
    for element_index, element_nodes in enumerate(all_element_nodes):
        if len(element_nodes) not in [3, 4, 6, 8]:
            error_collector.raise_error(
                f"Mesh: {mesh.name}: Invalid number of element nodes ({len(element_nodes)} nodes) for element index {element_index}. Should be 3, 4, 6, or 8"
            )
        max_node_index = max(element_nodes.max(), max_node_index)

    return max_node_index


def _validate_mesh(mesh, error_collector):
    """Validate a single mesh.

    Parameters
    ----------
    mesh : h5py.Group
        Mesh group to validate.
    error_collector : ErrorCollector
        Error collector instance.
    """
    element_labels = error_collector.checked_get(mesh, "element_labels")
    if element_labels is None:
        return

    if len(element_labels) == 0:
        error_collector.raise_error(f"No element labels in {mesh.name}")

    elements_shape = element_labels.shape
    if len(elements_shape) != 1:
        error_collector.raise_error("Invalid shape for element labels")

    n_elements = element_labels.shape[0]

    # Validate element nodes
    all_element_nodes = error_collector.checked_get(mesh, "element_nodes")
    if all_element_nodes is None:
        return

    max_node_index = _validate_element_nodes(
        mesh, all_element_nodes, n_elements, error_collector
    )

    # Validate element types
    element_types = error_collector.checked_get(mesh, "element_types")
    if element_types is not None:
        if len(element_types.shape) != 1:
            error_collector.raise_error("Invalid shape for element types")
        if element_types.shape[0] != n_elements:
            error_collector.raise_error(
                f"Mesh: {mesh.name}: Invalid length of element type array. Number of elements {element_types.shape[0]} != {n_elements}. Needs to match length of element labels."
            )

    # Validate node labels and nodes
    node_labels = error_collector.checked_get(mesh, "node_labels")
    if node_labels is None:
        return

    if len(node_labels.shape) != 1:
        error_collector.raise_error(f"Mesh: {mesh.name}: Invalid shape for node labels")

    n_nodes = node_labels.shape[0]
    if max_node_index >= n_nodes:
        error_collector.raise_error(
            f"Mesh: {mesh.name}: Invalid node index in element_nodes array: {max_node_index}. Should be < number of nodes: {n_nodes}"
        )

    nodes = error_collector.checked_get(mesh, "nodes")
    if nodes is None:
        return

    if len(nodes.shape) != 2:
        error_collector.raise_error(f"Mesh: {mesh.name}: Invalid shape for nodes")

    if nodes.shape[1] != 3:
        error_collector.raise_error(
            f"Mesh: {mesh.name}: Invalid shape for node labels. Second dimension of nodes should be 3"
        )

    if nodes.shape[0] != n_nodes:
        error_collector.raise_error(
            f"Mesh: {mesh.name}: Invalid length of node labels. Expected {n_nodes} but got {nodes.shape[0]}. Needs to match length of node labels."
        )


def _validate_meshes(meshes, error_collector, h5_file):
    """Validate all meshes in the file.

    Parameters
    ----------
    meshes : h5py.Group
        Meshes group to validate.
    error_collector : ErrorCollector
        Error collector instance.
    h5_file : Path | str
        Path of the file being validated.
    """
    if meshes is None:
        return

    if len(meshes) == 0:
        error_collector.raise_error(f"No mesh in {h5_file}")

    for mesh in meshes.values():
        _validate_mesh(mesh, error_collector)


def _validate_data_maps(data_maps, error_collector):
    """Validate all data maps in the file.

    Parameters
    ----------
    data_maps : h5py.Group
        Data maps group to validate.
    error_collector : ErrorCollector
        Error collector instance.
    """
    if data_maps is None:
        return

    for data_map in data_maps.values():
        reference_directions = error_collector.checked_get(
            data_map, "reference_directions"
        )
        if reference_directions is None:
            continue

        if len(reference_directions.shape) != 2:
            error_collector.raise_error(
                f"Data Map: {data_map.name}: Invalid shape for data map"
            )

        if reference_directions.shape[1] != 3:
            error_collector.raise_error(
                f"Data Map: {data_map.name}: Invalid shape for reference directions. Expected 3 components for reference direction, but got {reference_directions.shape[1]}"
            )


def validate_file(h5_file: Path | str, stop_on_first_error=False):
    """Validates a composite_cae HDF5 file.

    Throws an exception on the first error if `stop_on_first_error` is true. Otherwise, prints
    the errors to the console.

    Parameters
    ----------
    h5_file:
        Path of the file to validate
    stop_on_first_error:
        If True, stops on first error. Otherwise, lists all the errors found in the file.
    """
    error_collector = ErrorCollector(stop_on_first_error)
    with h5.File(h5_file, "r") as f:
        root = error_collector.checked_get(f, "composite_cae")
        if root is None:
            error_collector.raise_accumlated_errors()
            return

        # Validate components
        components = error_collector.checked_get(root, "components")
        _validate_components(f, components, error_collector, h5_file)

        # Validate material data
        material_data = error_collector.checked_get(root, "material_data")
        _validate_material_data(material_data, error_collector, h5_file)

        # Validate meshes
        meshes = error_collector.checked_get(root, "meshes")
        _validate_meshes(meshes, error_collector, h5_file)

        # Validate data maps
        data_maps = error_collector.checked_get(root, "data_maps")
        _validate_data_maps(data_maps, error_collector)

        error_collector.raise_accumlated_errors()
        print("Validation passed without error.")
