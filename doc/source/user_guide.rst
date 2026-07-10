.. _user_guide:

User guide
##########

Use this guide to work with the HDF5 composite CAE file format.

Overview
--------

**Ansys HDF5 composite CAE** is a Python package for working with the HDF5 composite CAE
format. It helps you exchange composite layup data between computer-aided engineering
(CAE) tools.

The package includes:

- **Format specification**: Structure of the HDF5 composite CAE format
- **File validation**: Tools to validate HDF5 files against the specification
- **File creation**: Tools to create compliant HDF5 composite CAE files
- **Example files**: Sample files that show the format's capabilities

Key concepts
------------

The HDF5 composite CAE format uses these three concepts:

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

Data maps define material orientation and geometric properties for each component.

Validate files
----------------

Use the provided tools to validate HDF5 files against the composite CAE specification.

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

To validate a file, run:

.. code-block:: bash

    validate_composite_cae_h5 my_h5_file.h5

This command checks whether the file conforms to the specification. It reports any issues.

Python API
~~~~~~~~~~

To validate a file programmatically, use:

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    try:
        validate_file("my_file.h5")
        print("File is valid!")
    except Exception as e:
        print(f"Validation failed: {e}")

The function returns ``True`` for a valid file. Otherwise, it raises an exception.

Create files
------------

Use the package to create HDF5 composite CAE files.

Create a minimal file
~~~~~~~~~~~~~~~~~~~~~

To create a minimal compliant file, use:

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

Use this file as a starting point. Then add your mesh, components, and data maps.

Work with example files
-----------------------

The package includes example HDF5 files that show the format's capabilities.

Locate example files
~~~~~~~~~~~~~~~~~~~~

To find the example files, run:

.. code-block:: bash

    show_composite_cae_h5_examples

This command prints the path to the examples.

Use example files
~~~~~~~~~~~~~~~~~

Use example files as references when you create your own files. Open them with HDFView or another HDF5 viewer to inspect their structure.

Further reading
---------------

- See the :ref:`specification` for file structure and format requirements.
- See the :ref:`api` for classes, functions, and methods.
- See :ref:`contribute` for development and contribution guidelines.

