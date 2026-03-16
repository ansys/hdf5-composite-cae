=========================
HDF5 composite CAE format
=========================

This Python package provides both documentation and Python tools to work with the HDF5 composite CAE format. For information on 
the format’s specifications, see :ref:`specification`.

You can access the example files and validation capabilities by installing the Python package with:

.. code::

    # Create virtual environment and activate it
    python -m venv .venv
    .venv/Scripts/activate.bat # Linux: source .venv/bin/activate

    # Install package
    pip install ansys-hdf5-composite-cae

The package contains a command-line tool ``validate_composite_cae_h5`` which checks if a H5 file conforms to the specification.

.. code::

    validate_composite_cae_h5 my_h5_file.h5

The package also contains multiple example H5 files. This command shows the location of the example files in your installation:

.. code::

    show_composite_cae_h5_examples

You can move to the location shown to inspect and use the example files.

.. note::
    HDF5 is a binary file format, so you need a viewer to open it. You can download one here:

    https://www.hdfgroup.org/download-hdfview/

Click the cards below to see the specifications and API reference.

.. grid:: 1 1 1 2
    :gutter: 2

    .. grid-item-card:: :octicon:`file-code` Composite CAE H5 specification
        :link: specification
        :link-type: doc

        Describes the specifications of the Composite CAE H5 format.

    .. grid-item-card:: :octicon:`code` API reference
        :link: api
        :link-type: doc

        Describes the public Python classes, methods, and functions.
