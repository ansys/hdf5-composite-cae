.. _user_guide:

User guide
##########

This guide explains how to work with the HDF5 composite CAE file format.

Overview
--------

**Ansys HDF5 composite CAE** is a Python package that provides documentation and tools
for working with the HDF5 composite CAE format. The format enables the exchange of
composite layup data between computer-aided engineering (CAE) tools.

The package includes:

- **Format specification**: Documentation of the HDF5 composite CAE format structure
- **File validation**: Tools to validate HDF5 files against the specification
- **File creation**: Utilities to create compliant HDF5 composite CAE files
- **Example files**: Sample files that demonstrate the format's capabilities

Key concepts
------------

The HDF5 composite CAE format is based on the following concepts:

Mesh
~~~~

Stores geometric information consisting of nodes and elements. The mesh forms the foundation 
for defining composite layups.

Component
~~~~~~~~~

Represents a layer in the composite structure. Each component references a data map and
the underlying mesh. Use components to define layers with different properties.

Data map
~~~~~~~~

Contains data associated with each element or node in the mesh, including:

- Thickness
- Reference direction
- Fiber direction

Data maps define the material orientation and geometric properties for each component.

Validate files
----------------

Use the provided tools to validate HDF5 files against the composite CAE specification.

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

Validate a file:

.. code-block:: bash

    validate_composite_cae_h5 my_h5_file.h5

This command checks whether the file conforms to the specification and reports any issues.

Python API
~~~~~~~~~~

Validate files programmatically:

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    try:
        validate_file("my_file.h5")
        print("File is valid!")
    except Exception as e:
        print(f"Validation failed: {e}")

The function returns ``True`` if the file is valid or raises an
exception if validation fails.

Create files
------------

Use the package to create HDF5 composite CAE files.

Create a minimal file
~~~~~~~~~~~~~~~~~~~~~

Create a minimal compliant file:

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

Use this file as a starting point and extend it with your own mesh, components, and data
maps.

Work with example files
-----------------

The package includes example HDF5 files that demonstrate the format's capabilities.

Locate example files
~~~~~~~~~~~~~~~~~~~~

To find the example files:

.. code-block:: bash

    show_composite_cae_h5_examples

This command prints the path to the example files.

Use example files
~~~~~~~~~~~~~~~~~

Use the example files as references when creating your own files. Open them with HDFView or 
another HDF5 viewer to inspect their structure and content.

Further reading
---------------

- See the :ref:`specification` for format details
- See the :ref:`api` for futher documentation
- See the :ref:`contribute` for contribution guidelines

