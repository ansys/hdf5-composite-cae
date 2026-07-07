.. _getting_started:

Getting started
###############

Use this section to install and start working with the HDF5 composite CAE package.

Installation
------------

Install the package using ``pip``:

.. code-block:: bash

    pip install ansys-hdf5-composite-cae

Development installation
------------------------

To install the package with all optional and development dependencies:

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

After installation, use the package from the command-line interface or Python API.

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

Validate an HDF5 file against the composite CAE specification:

.. code-block:: bash

    validate_composite_cae_h5 my_file.h5

View the location of example files:

.. code-block:: bash

    show_composite_cae_h5_examples

Python API
~~~~~~~~~~

Validate a file:

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    # Returns True if valid, raises an exception with details if invalid
    validate_file("my_file.h5")

Create a minimal file:

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

View HDF5 files
---------------

HDF5 is a binary format, so you need a viewer to inspect file contents.
You can download HDFView from the HDF Group website:

https://www.hdfgroup.org/download-hdfview/

Next steps
----------

- See the :ref:`user_guide` for detailed usage
- See the :ref:`specification` for format structure
- See the :ref:`api` for further documentation