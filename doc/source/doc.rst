===================================
HDF5 Composite CAE Specification
===================================

.. contents:: Table of Contents
   :depth: 2
   :local:



General information
===================

Node Types in HDF5 Tree
-----------------------

Container Node
~~~~~~~~~~~~~~

Group node which contains a list of object nodes of the same type.

**Examples:** fabrics, meshes, rosettes

Named Object Node
~~~~~~~~~~~~~~~~~

Node to specify an object. To avoid naming restrictions of HDF5 nodes, the external object name should be stored in the ``title`` attribute of the node.

The associated data of an object is stored in attributes of the object node or attached data nodes.

**Examples:** fabric, mesh, rosette

Link Node
~~~~~~~~~

Dependencies between the different nodes in the tree are stored using link nodes.

Data Node
~~~~~~~~~

Data nodes can either contain array data or scalar data in attributes.

Specification of Node Names
---------------------------

To provide smooth interoperability with most high-level HDF5 interfaces (for example PyTables), the HDF node names must match the (perl regexp) pattern ``'^[a-zA-Z_][a-zA-Z0-9_]*$'``. The names on the Nodes must be unique within each group.

General Comments
-----------------

The encoding of String attributes is UTF8.


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
     - "Ansys, Inc."
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

All properties are optional, if no unit system is specified the unit system of the importer is used. The different ``*_unit`` attributes have higher priority than the ``unit_system`` attribute. E.g if ``unit_system`` is SI and ``length_unit`` is mm, mm is used as a length unit.

composite_cae->global_coord_sys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4 by 3 array of double

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [dir3 x]     [dir3 y]     [dir3 z]

Defines the origin and directions of the origin for the entire model. Currently not supported by ansys.

Material Data
=============

material_data->fabrics->fabric(named)
-------------------------------------

material_data->fabrics->fabric(named)->orientations (Obsolete)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Array of double

.. code-block:: text

   [0, 45, -45]

.. note::
   This property is not written or read by ansys. It will be removed in the future.

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
     - EUR, USD, etc
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
     - Determines order of fabrics within stackup
   * - ``angle``
     - double
     - Angle of fabric within stackup

Meshes
======

meshes->mesh(named)->node_labels
--------------------------------

n by 1 array of int

.. code-block:: text

   [unique node id]

meshes->mesh(named)->nodes
--------------------------

n by 3 array of doubles

.. code-block:: text

   [node x]  [node y]  [node z]

meshes->mesh(named)->element_labels
-----------------------------------

n by 1 array of int

.. code-block:: text

   [unique element id]

meshes->mesh(named)->element_types
----------------------------------

n by 1 array of int

.. code-block:: text

   [element type]

Currently the following element types are defined:

- **3:** 3 node shell
- **4:** 4 node shell
- **6:** 6 node shell
- **8:** 8 node shell

The list of element types might be expanded in the future, for example using 108 and 120 for 8 and 20 node bricks.

meshes->mesh(named)->element_nodes
----------------------------------

n by m VLArray of int

.. code-block:: text

   [node 1] [node 2] … [node m]

Defines nodes of elements with node INDICES pointing directly to entries in the nodes/node_labels arrays.

The order of the nodes must correspond to the following indices:

- 3 nodes (linear triangle): I, J, K
- 4 nodes (linear rectangle): I, J, K, L
- 6 nodes (quadratic triangle): I, J, K, M, N, P
- 8 nodes (quadratic rectangle): I, J, K, L, M, N, O, P

.. note::
   Here a VLArray data set is used since the mesh can contain element of different types (refer to ``meshes->mesh(named)->element_types``)

meshes->mesh(named)->edge_sets->edge_set(named)
-----------------------------------------------

Array of unsigned

Array with node INDICES referencing the nodes in this set.

meshes->mesh(named)->element_sets->element_set(named)
-----------------------------------------------------

Array of unsigned

Array with element INDICES referencing the elements in this set.

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
     - aka step value. Global identifier. Determines the order of the plies (increasing from bottom to top)
   * - ``orientation``
     - double
     - nominal orientation angle relative to the reference direction
   * - ``mapping_type``
     - string
     -

.. note::
   The mapping_type is optional and will be detailed later. Since ACP allows to use multiple rosettes to define the reference direction within a ply, different mapping types (interpolation algorithms) are defined, such as "minimum distance", "minimum angle", etc.

components->component(named)->placement_coord_sys
-------------------------------------------------

4 by 3 array of double

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [normal x]   [normal y]   [normal z]

The placement_coord_sys is used for two things:

- The normal of the placement coordinate system is used to define the default offset direction of the layup.
- The origin and dir1 are used to define the starting point and the initial direction of the draping calculation, respectively.

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

- If the data_map contains a thickness, a "material" of type ``material_data->stackups`` is not supported
- If ``data_map->thickness`` is not defined the thickness is computed from ``cured_thickness`` if material is a "fabric" or the sum of the ``cured_thickness`` for all the "fabric" if material is a ``material_data->stackup``
- If matorient_1_angles is not present it set equal to ``component->orientation``
- If matorient_2_angles is not present it is computed as: matorient_2_angles = matorient_1_angles + 90°

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
   The possible values of the rosette mapping_type are not yet specified. FiberSIM defines "translational", "standard", and "rotational" mapping types. ACP defines "parallel", "radial", "cylindrical" and "spherical" as standard rosette types. The exact definition of this attribute has been postponed, because this is optional information to exchange, which it is not needed to map the orientation field of the plies correctly.

rosettes->rosette(named)->coord_sys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4 by 3 array of double

.. code-block:: text

   [origin x]   [origin y]   [origin z]
   [dir1 x]     [dir1 y]     [dir1 z]
   [dir2 x]     [dir2 y]     [dir2 z]
   [normal x]   [normal y]   [normal z]

Data Maps
=========

data_maps->data_map(named)->element_set/node/node_set
-----------------------------------------------------

Defines a link to an element set of a mesh or a link to an edge_set of a mesh. This defines the positions where the orientations, thicknesses etc are given.

data_maps->data_map(named)->reference_directions
------------------------------------------------

n by 3 array of double

Defines the reference directions absolutely with direction vectors.

data_maps->data_map(named)->normals
-----------------------------------

n by 3 array of double (Optional)

Defines the normal directions absolutely with direction vectors. If present they can be used to project the reference direction onto the plane defined by the normal.

data_maps->data_map(named)->matorient_1_angles
----------------------------------------------

n by 1 array of double (Optional)

Defines the material orientation 1 angles with respect to the reference direction and the given normal.

data_maps->data_map(named)->matorient_2_angles
----------------------------------------------

n by 1 array of double (Optional)

Defines the material orientation 2 angles with respect to the reference direction and the given normal.

data_maps->data_map(named)->thicknesses
---------------------------------------

n by 1 array of double (Optional)

Defines position dependent thickness values.

data_maps->data_map(named)->scalar_user_data->scalar_user_data(named)
---------------------------------------------------------------------

n by 1 array of double (Optional)

User defined scalar data fields. Only supported by ansys.


.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Attribute
     - Type
     - Values
   * - ``unit_type``
     - string
     - "dimensionless", "length", "mass", "time", "temp" (default: "dimensionless")

Component Groups
================

component_groups->component_group(named)
----------------------------------------

Optional

Component groups can be defined to store grouping information of components.

Change Log
==========

.. list-table::
   :widths: 15 50 15
   :header-rows: 1

   * - Date
     - Description
     - Author
   * - May 5, 2010
     - ACP – FiberSIM Interface Format Specification Rev 01
     - O. Koenig, M. Wintermantel
   * - June 5, 2010
     - HDF5 Composite CAE Data File Specification Proposal version 1.1
     - J. Grape, J. Koenig
   * - Aug 10, 2010
     - HDF5 Composite CAE Data File Specification Release Candidate 1 for stable version 1.0

       Latest modifications from EVEN:

       - Modified stackup definition slightly to take into account that links cannot have attributes
       - Proposing element type IDs to be used within mesh/elements array

       Latest modifications taken from Vistagy's feedback of Aug 9 2010:

       - Added ``composite_cae/temp_unit`` attribute
       - Added the proposed thickness map data to the specification. This extension also leads to a name change of the "orientation_map" to the more general "data_map". For consistency we also propose to change 'material_thickness' to 'thicknesses'
     - O. Koenig, U. Mennel, M. Wintermantel
   * - Aug 11, 2010
     - Minor updates in "Open Questions", added Section "Specification of Node Names"
     - O. Koenig, U. Mennel
   * - Aug 30, 2010
     - Upgrade specification to match all issues recently discussed with Vistagy via emails
     - O. Koenig
   * - Mar 17, 2011
     - Cleanup the document a little
     - O. Koenig
   * - Oct 17, 2014
     - Adding component_groups and component_group nodes
     - O. Koenig
   * - June 28, 2019
     - Adding some additional information
     - R. Roos
   * - January 24, 2020
     - Corrected name for matorient_angles: "mat_orient1_angles" to "matorient_1_angles" and "mat_orient2_angles" to "matorient_2_angles". Defined which fields in data_map are optional and specify what happens if optional nodes are missing. Clarified use of placement_coord_sys
     - J. von Rickenbach
   * - September 15, 2020
     - Mentioned that global_coord_sys is currently not supported. Correct what happens when matorient_1_angles are not present
     - J. von Rickenbach
   * - January 26, 2022
     - Mark ``material_data->fabrics->fabric(named)->orientations`` as obsolete
     - J. von Rickenbach
   * - February 4, 2022
     - Change Href to Softlink for items that have to be linked with a Softlink
     - J. von Rickenbach
   * - February 8, 2022
     - Correct datatype for element_labels, element_nodes and element_types (now int)

       - Clarified layer id
     - J. von Rickenbach
   * - February 17, 2022
     - Clarified units specification

       - Mark optional material properties as optional
     - J. von Rickenbach
   * - May 12, 2022
     - Add optional scalar_user_data data_map property
     - J. von Rickenbach
   * - May 31, 2022
     - Improved formatting, Removed outdated future plans section. Added missing rosettes in component
     - J. von Rickenbach
   * - May 22, 2023
     - Improve documentation of node order
     - J. von Rickenbach
   * - May 15, 2024
     - Complete supported units
     - J. v. Rickenbach
   * - June 21, 2024
     - Clarified orientation
     - Jan von Rickenbach
   * - April 14, 2024
     - Some clarifications
     - R. Roos
