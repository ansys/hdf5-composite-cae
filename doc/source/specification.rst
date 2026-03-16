.. _specification:
===================================
HDF5 composite CAE specifications
===================================

This document describes the specifications for the HDF5 composite CAE file format, which exchanges composite layup information between CAE tools.
The key layup concepts are:

* **Mesh**: You store geometrical information on the mesh, which consists of nodes and elements.
* **Component**: A component represents a layer. Each component references a data_map and the mesh.
* **Data map**: The data_map stores the geometrical information associated with each element or node in the mesh. 
This includes thickness, reference direction, and fiber direction.

.. note::
    HDF5 is a binary file format, so you need a viewer to open it. You can download one here:

    https://www.hdfgroup.org/download-hdfview/

Tree overview
=============

.. figure:: _static/tree.png
   :target: _static/tree.png
   :alt: HDF5 Composite CAE Specification Tree
   :width: 600px
   :align: center

   Click to view full size

.. contents:: Table of Contents
   :depth: 2
   :local:

General information
===================

Node Types in HDF5 tree
-----------------------

Container node
~~~~~~~~~~~~~~

A container node is a group node that contains a list of object nodes of the same type.

**Examples**: fabrics, meshes, rosettes

Named object node
~~~~~~~~~~~~~~~~~

A named object node represents a single object. To avoid the naming restrictions of HDF5 nodes, store the external object name in the ``title`` attribute.

Store the object's associated data in the node's attributes or in attached data nodes.

**Examples**: fabric, mesh, rosette

Link node
~~~~~~~~~

A link node stores the dependencies between nodes in the tree.

Data node
~~~~~~~~~

A data node stores either array data or scalar data in its attributes.

Specification of node names
---------------------------

To support interoperability with high-level interfaces (such as PyTables), HDF5 node names must match the Perl-compatible regular expression ``'^[a-zA-Z_][a-zA-Z0-9_]*$'``.
Node names must be unique within each group.

General comments
-----------------

All string attributes is UTF-8 encoding.


Root level nodes
=================

composite_cae
-------------

All attributes are optional.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Attribute
     - Type
     - Values
   * - ``format_version``
     - string
     - 1.0
   * - ``last_modified``
     - datestring
     - "2010-08-23 13:31:13Z"
   * - ``vendor``
     - string
     - "ansys, inc."
   * - ``unit_system``
     - string
     - "SI", "Imperial"
   * - ``length_unit``
     - string
     - "m", "cm", "mm", "um", "in"
   * - ``mass_unit``
     - string
     - "kg", "t", "g", "lbf", "lbm"
   * - ``time_unit``
     - string
     - "s"
   * - ``temp_unit``
     - string
     - "C", "K", "F"
   * - ``angles``
     - string
     - "deg", "rad"

If you do not specify a unit system, the importer uses its default unit system. The ``*_unit`` attributes take precedence over the ``unit_system`` attribute.
For example, if ``unit_system`` is set to "SI" and ``length_unit`` is "mm," the length unit is "mm.""

composite_cae->global_coord_sys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4 by 3 array of doubles that defines the origin and its directions for the entire model. 

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [dir3 x]     [dir3 y]     [dir3 z]

This attribute is currently not supported by Ansys.

Material data
=============

material_data->fabrics->fabric(named)
-------------------------------------

material_data->fabrics->fabric(named)->orientations (Obsolete)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Array of doubles.

.. code-block:: text

   [0, 45, -45]

.. note::
   Ansys does not read or write this property. It will be removed in a future release.

material_data->fabrics->fabric(named)->mechanical
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``architecture``
     - string (optional)
     - uni, woven
   * - ``weight_per_area``
     - double
     -
   * - ``cured_thickness``
     - double
     -
   * - ``E1``
     - double (optional)
     -
   * - ``E2``
     - double (optional)
     -
   * - ``E3``
     - double (optional)
     -
   * - ``G12``
     - double (optional)
     -
   * - ``G23``
     - double (optional)
     -
   * - ``G31``
     - double (optional)
     -
   * - ``v12``
     - double (optional)
     -
   * - ``v13``
     - double (optional)
     -
   * - ``v23``
     - double (optional)
     -
   * - ``alpha1``
     - double (optional)
     -
   * - ``alpha2``
     - double (optional)
     -
   * - ``alpha_ref_temp``
     - double (optional)
     -

material_data->fabrics->fabric(named)->cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``currency``
     - string
     - EUR, USD, etc
   * - ``cost_per_area``
     - double
     -

material_data->stackups->stackup(named)->cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``currency``
     - string
     - EUR, USD, etc.
   * - ``cost_per_area``
     - double
     -

material_data->stackups->stackup(named)->fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``number``
     - unsigned
     - Determines order of fabrics within stackup.
   * - ``angle``
     - double
     - Angle of fabric within stackup.

Meshes
======

meshes->mesh(named)->node_labels
--------------------------------

n by 1 array of integers.

.. code-block:: text

   [unique node id]

meshes->mesh(named)->nodes
--------------------------

n by 3 array of doubles.

.. code-block:: text

   [node x]  [node y]  [node z]

meshes->mesh(named)->element_labels
-----------------------------------

n by 1 array of integers.

.. code-block:: text

   [unique element id]

meshes->mesh(named)->element_types
----------------------------------

n by 1 array of integers.

.. code-block:: text

   [element type]

Currently, the following element types are defined:

- **3:** 3 node shell
- **4:** 4 node shell
- **6:** 6 node shell
- **8:** 8 node shell

The list of element types may be expanded in future releases, for example by using 108 and 120 for 8- and 20-node bricks.

meshes->mesh(named)->element_nodes
----------------------------------

n by m VLArray of integers.

.. code-block:: text

   [node 1] [node 2] … [node m]

Defines the element's nodes, with node indices that point directly to entries in the nodes and node_labels arrays.

The order of the nodes must follow the indices shown below:

- 3 nodes (linear triangle): I, J, K
- 4 nodes (linear rectangle): I, J, K, L
- 6 nodes (quadratic triangle): I, J, K, M, N, P
- 8 nodes (quadratic rectangle): I, J, K, L, M, N, O, P

.. figure:: _static/elements.png
   :target: _static/elements.png
   :alt: Element Types
   :width: 400px
   :align: center

   Click to view full size.

.. note::
   A VLArray data set is used here because the mesh can contain element of different types (see ``meshes->mesh(named)->element_types``).


meshes->mesh(named)->edge_sets->edge_set(named)
-----------------------------------------------

Array of unsigned integers. Contains node indices that reference the nodes in this set.

meshes->mesh(named)->element_sets->element_set(named)
-----------------------------------------------------

Array of unsigned integers. Contains element indices that reference the elements in this set.

Components
==========

components->component(named)
----------------------------

Attributes:

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``type``
     - string
     - ply, core, etc.
   * - ``layer_id``
     - integer
     - The step value and global identifier. It determines the order of the plies (increasing from bottom to top).
   * - ``orientation``
     - double
     - The nominal orientation angle relative to the reference direction.
   * - ``mapping_type``
     - string
     -

.. note::
   The mapping_type attribute is optional and will be detailed later; because ACP can use multiple rosettes 
   to define a ply's reference direction, several mapping types are defined, including interpolation algorithms such as "minimum distance" and "minimum angle."

components->component(named)->placement_coord_sys
-------------------------------------------------

4 by 3 array of doubles.

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [normal x]   [normal y]   [normal z]

The placement_coord_sys is used for two purposes:

- Its normal defines the default offset direction of the layup.
- Its origin and dir1 define the starting point and initial direction of the draping calculation.

components->component(named)->material
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Softlink**

Defines the ply material and refers to an object in ``material_data->fabrics`` or ``material_data->stackups``.

components->component(named)->element_set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Softlink**

Defines a link to an element set of a mesh and specifies the ply extent.

components->component(named)->data_map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Softlink**

Defines a link to the data map of this component.

The following restrictions and rules apply:

- If the data_map contains a thickness, a "material" of type ``material_data->stackups`` is not supported.
- If ``data_map->thickness`` is not defined, the thickness is computed from ``cured_thickness`` when the material is a "fabric," or from the sum of all ``cured_thickness`` values when ``material_data->stackup``.
- If matorient_1_angles is not present, it set equal to ``component->orientation``.
- If matorient_2_angles is not present, it is computed as: matorient_2_angles = matorient_1_angles + 90°.

components->component(named)->rosettes->rosette(named)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Softlink (Optional)**

Defines a link to the rosettes of this component.

Rosettes
========

rosettes->rosette(named)
------------------------

Attributes:

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``mapping_type``
     - string
     -

.. note::
   The possible values of the rosette mapping_type are not yet specified. FiberSIM defines the mapping types "translational," "standard," and "rotational." 
   ACP defines the standard rosette types "parallel," "radial," "cylindrical," and "spherical." The exact definition of this attribute has been postponed 
   because this information is optional and is not required to map the ply orientation field correctly.

rosettes->rosette(named)->coord_sys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4 by 3 array of doubles.

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [normal x]   [normal y]   [normal z]

Data maps
=========

data_maps->data_map(named)->element_set/node/node_set
-----------------------------------------------------

Defines a link to an element set of a mesh or to an edge_set of a mesh. This link specifies the positions where the orientations, thicknesses, and other values are defined.

data_maps->data_map(named)->reference_directions
------------------------------------------------

n by 3 array of doubles.

Defines the reference directions using absolute direction vectors.

data_maps->data_map(named)->normals
-----------------------------------

n by 3 array of doubles (optional).

Defines the normal directions using absolute direction vectors. If present, these vectores can be used to project the reference direction onto the plane defined by the normal.

data_maps->data_map(named)->matorient_1_angles
----------------------------------------------

n by 1 array of doubles (optional).

Defines the material orientation 1 angles with respect to the reference direction and the given normal.

data_maps->data_map(named)->matorient_2_angles
----------------------------------------------

n by 1 array of doubles (optional).

Defines the material orientation 2 angles with respect to the reference direction and the given normal.

data_maps->data_map(named)->thicknesses
---------------------------------------

n by 1 array of doubles (optional).

Defines position dependent thickness values.

data_maps->data_map(named)->scalar_user_data->scalar_user_data(named)
---------------------------------------------------------------------

n by 1 array of doubles (optional).

User-defined scalar data fields. Only supported by Ansys.


.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Values
   * - ``unit_type``
     - string
     - "dimensionless", "length", "mass", "time", "temp" (default: "dimensionless")

Component groups
================

component_groups->component_group(named)
----------------------------------------

Optional.

Component groups can be defined to store grouping information of components.



Change log
==========

.. list-table::
   :widths: 15 50
   :header-rows: 1

   * - Date
     - Description
   * - May 5, 2010
     - ACP–FiberSIM Interface Format Specification Rev 01
   * - June 5, 2010
     - HDF5 Composite CAE Data File Specification Proposal version 1.1
   * - Aug 10, 2010
     - HDF5 Composite CAE Data File Specification Release Candidate 1 for stable version 1.0.
   * - Aug 11, 2010
     - Minor updates in "Open Questions", added Section "Specification of Node Names"
   * - Aug 30, 2010
     - Upgrade specification to match all issues recently discussed with Vistagy via emails
   * - Mar 17, 2011
     - Cleanup the document a little
   * - Oct 17, 2014
     - Adding component_groups and component_group nodes
   * - June 28, 2019
     - Adding some additional information
   * - January 24, 2020
     - Corrected name for matorient_angles: "mat_orient1_angles" to "matorient_1_angles" and "mat_orient2_angles" to "matorient_2_angles". Defined which fields in data_map are optional and specify what happens if optional nodes are missing. Clarified use of placement_coord_sys
   * - September 15, 2020
     - Mentioned that global_coord_sys is currently not supported. Correct what happens when matorient_1_angles are not present
   * - January 26, 2022
     - Mark ``material_data->fabrics->fabric(named)->orientations`` as obsolete
   * - February 4, 2022
     - Change Href to Softlink for items that have to be linked with a Softlink
   * - February 8, 2022
     - Correct datatype for element_labels, element_nodes and element_types (now int), clarified layer id
   * - February 17, 2022
     - Clarified units specification, Mark optional material properties as optional
   * - May 12, 2022
     - Add optional scalar_user_data data_map property
   * - May 31, 2022
     - Improved formatting, Removed outdated future plans section. Added missing rosettes in component
   * - May 22, 2023
     - Improve documentation of node order
   * - May 15, 2024
     - Complete supported units
   * - June 21, 2024
     - Clarified orientation
   * - April 14, 2024
     - Some clarifications
