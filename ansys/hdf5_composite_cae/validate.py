# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

import logging
from pathlib import Path

import h5py as h5

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__all__ = ["validate_file"]


def _checked_get_setup(throw):
    def checked_get(obj, key):
        try:
            return obj[key]
        except Exception as e:
            err = f"Missing key {key} at {obj.name}"
            if throw:
                raise RuntimeError(err) from e
            log.error(err)

    return checked_get


def _check_attr_setup(throw):
    def check_attr(obj, attr):
        try:
            return obj.attrs[attr]
        except Exception as e:
            err = f"Missing attribute {attr} at {obj.name}"
            if throw:
                raise RuntimeError(err) from e
            log.error(err)

    return check_attr


def _raise_error_setup(throw):
    def raise_error(error):
        if throw:
            raise RuntimeError(error)
        log.error(error)

    return raise_error


def _check_softlink(f, path: str, throw):
    link = f.get(path, getlink=True)

    if not isinstance(link, h5.SoftLink):
        _raise_error_setup(throw)(f"{path} needs to be a softlink")


def validate_file(h5_file: Path | str, stop_on_first_error=False):
    """Validates a composite_cae hdf5 file.

    Throws an exception on the first error if `stop_on_first_error` is true. Otherwise, prints
    the errors to the console.

    Parameters
    ----------
    h5_file:
        Path of the file to validate
    stop_on_first_error:
        If True, stops on first error. Otherwise, lists all the errors found in the file.
    """
    raise_error = _raise_error_setup(stop_on_first_error)
    checked_get = _checked_get_setup(stop_on_first_error)

    with h5.File(h5_file, "r") as f:
        root = checked_get(f, "composite_cae")
        components = checked_get(root, "components")
        if len(components) == 0:
            raise RuntimeError(f"No components in {h5_file}")
        for component in components.values():
            # nothing required
            material = checked_get(component, "material")
            _check_softlink(f, material.name, stop_on_first_error)
            element_set = checked_get(component, "element_set")
            _check_softlink(f, element_set.name, stop_on_first_error)
            data_map = checked_get(component, "data_map")
            _check_softlink(f, data_map.name, stop_on_first_error)

        material_data = checked_get(root, "material_data")
        fabrics = checked_get(material_data, "fabrics")

        if len(fabrics) == 0:
            raise RuntimeError(f"No fabrics in {h5_file}")

        for _ in fabrics.values():
            pass
        #  mechanical = checked_get(fabric, "mechanical")
        #  _ = check_attr(mechanical, "weight_per_area")
        #  _ = check_attr(mechanical, "cured_thickness")

        #  cost = checked_get(fabric, "cost")
        #  _ = check_attr(cost, "currency")
        #  _ = check_attr(cost, "cost_per_area")

        meshes = checked_get(root, "meshes")
        if len(meshes) == 0:
            raise_error(f"No mesh in {h5_file}")

        for mesh in meshes.values():
            element_labels = checked_get(mesh, "element_labels")

            if len(element_labels) == 0:
                raise_error(f"No element labels in {mesh.name}")

            elements_shape = element_labels.shape
            if len(elements_shape) != 1:
                raise_error("Invalid shape for element labels")

            n_elements = element_labels.shape[0]

            all_element_nodes = checked_get(mesh, "element_nodes")

            if len(all_element_nodes) != n_elements:
                raise_error(
                    f"Mesh: {mesh.name}: Invalid number of element nodes in {mesh.name}. Expected {n_elements} but got {len(all_element_nodes)}"
                )

            max_node_index = 0
            for element_index, element_nodes in enumerate(all_element_nodes):
                if len(element_nodes) not in [3, 4, 6, 8]:
                    raise_error(
                        f"Mesh: {mesh.name}: Invalid number of element nodes ({len(element_nodes)} nodes) for element index {element_index}. Should be 3, 4, 6, or 8"
                    )
                max_node_index = max(element_nodes.max(), max_node_index)

            # Optional
            #   _ = checked_get(mesh, "element_sets")
            #   _ = checked_get(mesh, "edge_sets")
            element_types = checked_get(mesh, "element_types")

            if len(element_types.shape) != 1:
                raise_error("Invalid shape for element labels")
            if element_types.shape[0] != n_elements:
                raise_error(
                    f"Mesh: {mesh.name}: Invalid length of element type array. Number of elements {element_types.shape[0]} != {n_elements}. Needs to match length of element labels."
                )

            node_labels = checked_get(mesh, "node_labels")
            if len(node_labels.shape) != 1:
                raise_error(f"Mesh: {mesh.name}: Invalid shape for node labels")

            n_nodes = node_labels.shape[0]
            if max_node_index >= n_nodes:
                raise_error(
                    f"Mesh: {mesh.name}: Invalid node index in element_nodes array: {max_node_index}. Should be < number of nodes: {n_nodes}"
                )

            nodes = checked_get(mesh, "nodes")
            if len(nodes.shape) != 2:
                raise_error(f"Mesh: {mesh.name}: Invalid shape for nodes")

            if nodes.shape[1] != 3:
                raise_error(
                    f"Mesh: {mesh.name}: Invalid shape for node labels. Second dimension of nodes should be 3"
                )

            if nodes.shape[0] != n_nodes:
                raise_error(
                    f"Mesh: {mesh.name}: Invalid length of node labels. Expected {n_nodes} but got {nodes.shape[0]}. Needs to match length of node labels."
                )

        data_maps = checked_get(root, "data_maps")
        for data_map in data_maps.values():
            reference_directions = checked_get(data_map, "reference_directions")
            if len(reference_directions.shape) != 2:
                raise_error(f"Data Map: {data_map.name}: Invalid shape for data map")

            if reference_directions.shape[1] != 3:
                raise_error(
                    f"Data Map: {data_map.name}: Invalid shape for reference directions. Expected 3 components for reference direction, but got {reference_directions.shape[1]}"
                )
