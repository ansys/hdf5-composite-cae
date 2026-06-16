.. _getting_started:

***************
Getting started
***************

This section provides instructions for installing and getting started with the HDF5 Composite CAE package.

Installation
============

You can install the HDF5 Composite CAE package using ``pip``:

.. code-block:: bash

    pip install ansys-hdf5-composite-cae

Development installation
========================

For a development installation with all optional dependencies, follow these steps:

.. code-block:: bash

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

Quick start
===========

Once installed, you can start using the package through either the command-line interface or Python API.

Command-line interface
----------------------

Validate an HDF5 file against the composite CAE specification:

.. code-block:: bash

    validate_composite_cae_h5 my_file.h5

View the location of example files:

.. code-block:: bash

    show_composite_cae_h5_examples

Python API
----------

Validate a file
~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    # Returns True if valid, raises an exception with details if invalid
    validate_file("my_file.h5")

Create a minimal HDF5 file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

Viewing HDF5 files
==================

HDF5 is a binary file format, so you need a viewer to open and inspect it.
You can download the HDFView application here:

https://www.hdfgroup.org/download-hdfview/

Next steps
==========

- Check out the :ref:`user_guide` for more detailed information
- Read the :ref:`specification` to understand the format structure
- Explore the :ref:`api` for detailed API documentation


