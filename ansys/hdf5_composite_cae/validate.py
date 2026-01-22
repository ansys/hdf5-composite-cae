# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# Unauthorized use, distribution, or duplication is prohibited.

import logging
from pathlib import Path

import h5py as h5

logging.basicConfig(level=logging.ERROR, format="%(message)s")
log = logging.getLogger(__name__)

__all__ = ["validate_file"]


class ErrorCollector:
    def __init__(self, throw_on_first_error: bool):
        self._throw_on_first_error = throw_on_first_error
        self._errors = []

    def checked_get(self, obj, key: str):
        try:
            return obj[key]
        except Exception:
            err = f"Missing key '{key}' at {obj.name}"
            self.raise_error(err)

    def raise_error(self, error):
        if self._throw_on_first_error:
            raise RuntimeError(error)
        self._errors.append(error)

    def check_softlink(self, f, path: str):
        link = f.get(path, getlink=True)

        if not isinstance(link, h5.SoftLink):
            self.raise_error(f"{path} needs to be a softlink")

    def raise_accumulated_errors(self):
        if len(self._errors) > 0:
            raise RuntimeError("\n" + "\n".join(self._errors))


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
    error_collector = ErrorCollector(stop_on_first_error)
    with h5.File(h5_file, "r") as f:
        root = error_collector.checked_get(f, "composite_cae")
        components = error_collector.checked_get(root, "components")
        if components is not None:
            if len(components) == 0:
                error_collector.raise_error(f"No components in {h5_file}")
            for component in components.values():
                # nothing required
                material = error_collector.checked_get(component, "material")
                error_collector.check_softlink(f, material.name)
                element_set = error_collector.checked_get(component, "element_set")
                error_collector.check_softlink(f, element_set.name)
                data_map = error_collector.checked_get(component, "data_map")
                error_collector.check_softlink(f, data_map.name)

        material_data = error_collector.checked_get(root, "material_data")
        fabrics = None
        if material_data is not None:
            fabrics = error_collector.checked_get(material_data, "fabrics")

        if fabrics is not None and len(fabrics) == 0:
            error_collector.raise_error(f"No fabrics in {h5_file}")

        meshes = error_collector.checked_get(root, "meshes")
        if meshes is not None:
            if len(meshes) == 0:
                error_collector.raise_error(f"No mesh in {h5_file}")

            for mesh in meshes.values():
                element_labels = error_collector.checked_get(mesh, "element_labels")

                if len(element_labels) == 0:
                    error_collector.raise_error(f"No element labels in {mesh.name}")

                elements_shape = element_labels.shape
                if len(elements_shape) != 1:
                    error_collector.raise_error("Invalid shape for element labels")

                n_elements = element_labels.shape[0]

                all_element_nodes = error_collector.checked_get(mesh, "element_nodes")

                if len(all_element_nodes) != n_elements:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid number of element nodes in {mesh.name}. Expected {n_elements} but got {len(all_element_nodes)}"
                    )

                max_node_index = 0
                for element_index, element_nodes in enumerate(all_element_nodes):
                    if len(element_nodes) not in [3, 4, 6, 8]:
                        error_collector.raise_error(
                            f"Mesh: {mesh.name}: Invalid number of element nodes ({len(element_nodes)} nodes) for element index {element_index}. Should be 3, 4, 6, or 8"
                        )
                    max_node_index = max(element_nodes.max(), max_node_index)

                # Optional
                #   _ = error_collector.checked_get(mesh, "element_sets")
                #   _ = error_collector.checked_get(mesh, "edge_sets")
                element_types = error_collector.checked_get(mesh, "element_types")

                if len(element_types.shape) != 1:
                    error_collector.raise_error("Invalid shape for element labels")
                if element_types.shape[0] != n_elements:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid length of element type array. Number of elements {element_types.shape[0]} != {n_elements}. Needs to match length of element labels."
                    )

                node_labels = error_collector.checked_get(mesh, "node_labels")
                if len(node_labels.shape) != 1:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid shape for node labels"
                    )

                n_nodes = node_labels.shape[0]
                if max_node_index >= n_nodes:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid node index in element_nodes array: {max_node_index}. Should be < number of nodes: {n_nodes}"
                    )

                nodes = error_collector.checked_get(mesh, "nodes")
                if len(nodes.shape) != 2:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid shape for nodes"
                    )

                if nodes.shape[1] != 3:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid shape for node labels. Second dimension of nodes should be 3"
                    )

                if nodes.shape[0] != n_nodes:
                    error_collector.raise_error(
                        f"Mesh: {mesh.name}: Invalid length of node labels. Expected {n_nodes} but got {nodes.shape[0]}. Needs to match length of node labels."
                    )

        data_maps = error_collector.checked_get(root, "data_maps")
        if data_maps is not None:
            for data_map in data_maps.values():
                reference_directions = error_collector.checked_get(
                    data_map, "reference_directions"
                )
                if len(reference_directions.shape) != 2:
                    error_collector.raise_error(
                        f"Data Map: {data_map.name}: Invalid shape for data map"
                    )

                if reference_directions.shape[1] != 3:
                    error_collector.raise_error(
                        f"Data Map: {data_map.name}: Invalid shape for reference directions. Expected 3 components for reference direction, but got {reference_directions.shape[1]}"
                    )

    error_collector.raise_accumulated_errors()
