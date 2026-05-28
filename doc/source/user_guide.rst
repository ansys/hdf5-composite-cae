.. _user_guide:

**********
User guide
**********

This user guide provides detailed information about working with the HDF5 Composite CAE format.

Overview
========

**Ansys HDF5 Composite CAE** is a Python package that provides both documentation and tools
for working with the HDF5 composite CAE file format. This format enables the exchange of
composite layup information between Computer-Aided Engineering (CAE) tools.

The library offers:

- **Format Specification**: Complete documentation of the HDF5 composite CAE file format structure
- **File Validation**: Command-line and Python API tools to validate HDF5 files against the specification
- **File Creation**: Utilities to create compliant HDF5 composite CAE files
- **Example Files**: A collection of sample files demonstrating the format's capabilities

Key concepts
============

The HDF5 composite CAE format is built around several core concepts:

Mesh
----

Stores geometrical information consisting of nodes and elements. The mesh provides the
geometric foundation for defining composite layups.

Component
---------

Represents a layer in the composite structure. Each component references a data map and
the underlying mesh. Components allow you to define multiple layers with different properties.

Data map
--------

Contains geometrical information associated with each element or node in the mesh, including:

- Thickness values
- Reference direction
- Fiber direction

Data maps provide the detailed material orientation and geometric data for each component.

Validating files
================

The package provides tools to validate HDF5 files against the composite CAE specification.

Using the command-line interface
---------------------------------

The simplest way to validate a file is using the command-line tool:

.. code-block:: bash

    validate_composite_cae_h5 my_h5_file.h5

This command checks if the file conforms to the specification and reports any issues found.

Using the Python API
--------------------

You can also validate files programmatically:

.. code-block:: python

    from ansys.hdf5_composite_cae import validate_file

    try:
        validate_file("my_file.h5")
        print("File is valid!")
    except Exception as e:
        print(f"Validation failed: {e}")

The ``validate_file`` function returns ``True`` if the file is valid, or raises an
exception with detailed information if validation fails.

Creating files
==============

The package provides utilities to create HDF5 composite CAE files.

Creating a minimal file
-----------------------

You can create a minimal compliant HDF5 file as a starting point:

.. code-block:: python

    from ansys.hdf5_composite_cae import create_minimal_h5_file

    create_minimal_h5_file("output.h5")

This creates a basic file that conforms to the specification. You can then extend
this file with your own mesh, components, and data maps.

Working with example files
===========================

The package includes several example HDF5 files that demonstrate the format's capabilities.

Locating example files
----------------------

To find the example files in your installation:

.. code-block:: bash

    show_composite_cae_h5_examples

This command displays the location of the example files. You can navigate to this
directory to inspect and use the files.

Using example files
-------------------

The example files demonstrate different aspects of the format and can serve as
references for creating your own files. Use HDFView or another HDF5 viewer to
explore their structure.

Best practices
==============

When working with HDF5 composite CAE files, consider these best practices:

1. **Always validate**: Run validation on files before exchanging them with other tools
2. **Use meaningful names**: Give descriptive names to components and data maps
3. **Document your data**: Use HDF5 attributes to add metadata and documentation
4. **Start with examples**: Use the provided example files as templates for your own files
5. **Check the specification**: Refer to the :ref:`specification` for detailed format requirements

Further reading
===============

- :ref:`specification`: Detailed format specification
- :ref:`api`: Complete API reference
- :ref:`contribute`: Information on contributing to the project

