.. _getting_started:

Getting started
###############

Use this guide to install and start working with the HDF5 composite CAE package.

Installation
------------

Install the package using ``pip``:

.. code-block:: bash

    pip install ansys-hdf5-composite-cae

Development installation
------------------------

Install the package with all optional and development dependencies:

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
-----------

After installation, you can use the package from the command-line interface or Python API.

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

To validate an HDF5 file against the composite CAE specification, run:

.. code-block:: bash

    validate_composite_cae_h5 my_file.h5

To view the location of the example files, run:

.. code-block:: bash

    show_composite_cae_h5_examples

Python API
~~~~~~~~~~

To validate a file, use:

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    # Returns True if valid, raises an exception with details if invalid
    validate_file("my_file.h5")

To create a minimal file, use:

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

View HDF5 files
---------------

You need a viewer to inspect HDF5 file contents.
You can download HDFView from the HDF Group website:

https://www.hdfgroup.org/download-hdfview/

Next steps
----------

- See the :ref:`user_guide` for concepts, workflows, and examples.
- See the :ref:`specification` page for file structure and format requirements.
- See the :ref:`api` for classes, functions, and methods.