=========================
HDF5 Composite CAE Format
=========================

This python package provides documentation as well as python tools to work with the HDF5 Composite CAE format. The specification
of the format can be found here :ref:`specification`.

To use the validation capabilities and access the example files, the python package needs to be installed with:

.. code::

    # Create virtual environment and activate it
    python -m venv .venv
    .venv\Scripts\activate.bat # Linux: source .venv/bin/activate

    # Install package
    pip install ansys-hdf5-composite-cae

This installs a command line tool ``validate_composite_cae_h5`` which can be used to check if a given h5 file conforms to the specification.


.. code::

    validate_composite_cae_h5 my_h5_file.h5


The package comes with a number of example h5 files. The following command shows the location of the example files in your installation:


.. code::

    show_composite_cae_h5_examples

Move to the shown location to inspect and use the example files.

.. note::
    Since hdf5 is a binary format, you need a viewer to look at the file which you can find here:

    https://www.hdfgroup.org/download-hdfview/

Click below to access the specification and the API reference of the module.

.. grid:: 1 1 1 2
    :gutter: 2

    .. grid-item-card:: :octicon:`file-code` Composite CAE H5 specification
        :link: specification
        :link-type: doc

        Contains the Specification of the Composite CAE H5 format

    .. grid-item-card:: :octicon:`code` API reference
        :link: api
        :link-type: doc

        Describes the public Python classes, methods, and functions.
