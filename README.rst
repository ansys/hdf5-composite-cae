HDF5 Composite CAE
==================

|pyansys| |python| |pypi| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5+9ioKhgYGBgYGD4////MhoG+v////8/Pz8/AwMDAwMA+gD7/+3bt4uLi2tqaiorK+vo6Ojr6+vt7e3x8fHy8vLx8fHy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8fHw8PDv7+/r6+vo6Ojn5+fn5+fm5ubm5ubl5eXk5OTj4+Pi4uLh4eHh4eHg4ODf39/e3t7d3d3c3Nza2trbf39/c3NzbGxsbGxsbGxsa2trattsa2tra2tra2tra2tra2tra2tra2tra2tra2tra2tra2trattsa2tratt7e3t7e3t7e3tra2tra2tra2tra2tra2tra2trbWxsb////////7AAAAA0JREFUeNqNkF1OAyEUhI+Pj9/////f39/c3Nzb29va2tra2trZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2Nj4/////v7+7u7u7Ozs7Ozs6+vr6urq6enp6Ojo5+fn5ubm5OTk4+Pj4ODg39/f3d3d2dnZ2NjY19fX1dXV0tLS0NDQz8/Pzc3Ny8vLycnJx8fHxcXFw8PDwsLCv7+/vb29ubm5t7e3tbW1s7Ozr6+vra2tq6urqamppaWloqKinp6enJycmJiYlZWVk5OTkJCQjo6Oi4uLiYmJh4eHhYWFg4ODgYGBf39/fX19e3t7eXl5d3d3dXV1c3NzbW1ta2trZ2dnY2NjX19fW1tbV1dXU1NTT09PS0tLR0dHQ0NDPz8/Ozs7MzMzKysrIyMjGxsbExMTCwsLAwMC/v7+9vb26urq4uLi2tra0tLSysrKwsLCurq6srKyqqqqoqKimpqakpKSioqKgoKCenp6cnJyampqYmJiWlpaUlJSSkpKQkJCOjo6MjIyKioqIiIiGhoaEhISCgoKAgIB+fn58fHx6enp4eHh2dnZ0dHRycnJwcHBubm5sbGxqampnZ2dlZWVjY2NeXl5cXFxaWlpXV1dVVVVTU1NRUVFPT09NTU1LS0tJSUlHR0dFRUVDQ0M/Pz89PT07Ozs5OTk3Nzc1NTUzMzMxMTEvLy8tLS0rKysn
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-hdf5-composite-cae?logo=pypi
   :target: https://pypi.org/project/ansys-hdf5-composite-cae/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-hdf5-composite-cae.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-hdf5-composite-cae
   :alt: PyPI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys-internal/hdf5-composite-cae/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys-internal/hdf5-composite-cae/main
   :alt: pre-commit.ci status


Overview
--------

**Ansys HDF5 Composite CAE** is a Python package that provides both documentation and tools
for working with the HDF5 composite CAE file format. This format enables the exchange of
composite layup information between Computer-Aided Engineering (CAE) tools.

The library offers:

- **Format Specification**: Complete documentation of the HDF5 composite CAE file format structure
- **File Validation**: Command-line and Python API tools to validate HDF5 files against the specification
- **File Creation**: Utilities to create compliant HDF5 composite CAE files
- **Example Files**: A collection of sample files demonstrating the format's capabilities

Key concepts in the HDF5 composite CAE format include:

- **Mesh**: Stores geometrical information consisting of nodes and elements
- **Component**: Represents a layer, referencing a data map and the mesh
- **Data Map**: Contains geometrical information (thickness, reference direction, fiber direction)
  associated with each element or node in the mesh


Installation
------------

Install the package using ``pip``:

.. code:: bash

    pip install ansys-hdf5-composite-cae

For a development installation with all optional dependencies:

.. code:: bash

    # Install uv package manager
    # See: https://docs.astral.sh/uv/getting-started/installation/

    # Create virtual environment with Python >= 3.10
    uv venv --python 3.12

    # Activate the virtual environment
    # Windows:
    .venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate

    # Install package with all development dependencies
    uv sync --all-groups


Usage
-----

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

Validate an HDF5 file against the composite CAE specification:

.. code:: bash

    validate_composite_cae_h5 my_file.h5

View the location of example files:

.. code:: bash

    show_composite_cae_h5_examples


Python API
~~~~~~~~~~

**Validate a file:**

.. code:: python

    from ansys.hdf5_composite_cae import validate_file

    # Returns True if valid, raises an exception with details if invalid
    validate_file("my_file.h5")

**Create a minimal HDF5 file:**

.. code:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")


Documentation
-------------

For comprehensive information, including detailed specifications of the HDF5 composite CAE format
and complete API reference, visit the `official documentation <https://hdf5-composite-cae.docs.pyansys.com/>`_.

The documentation includes:

- Complete format specification with detailed descriptions of all nodes and attributes
- API reference for all public classes, methods, and functions
- Example files demonstrating various use cases
- Getting started guides and tutorials


.. note::
    HDF5 is a binary file format. To inspect HDF5 files visually, download HDFView from:
    https://www.hdfgroup.org/download-hdfview/


Build documentation
--------------------

.. code:: bash
    python scripts/build.py build_doc


Contributing
------------

For information about contributing to this project, see the `CONTRIBUTING.md <CONTRIBUTING.md>`_ file.

All contributions are subject to the project's `Code of Conduct <CODE_OF_CONDUCT.md>`_.


License
-------

This project is licensed under the MIT License. See the `LICENSE <LICENSE>`_ file for details.

Copyright (c) 2026 ANSYS, Inc. All rights reserved.

