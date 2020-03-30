# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "FreeCAD OOFEM mesh writer"
__author__ = "Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"

## @package importOofemMesh
#  \ingroup FEM
#  \brief FreeCAD OOFEM mesh writer for FEM workbench

import FreeCAD

from femmesh import meshtools


# ************************************************************************************************
# ********* generic FreeCAD import and export methods ********************************************
# names are fix given from FreeCAD, these methods are called from FreeCAD
# they are set in FEM modules Init.py

if open.__module__ == "__builtin__":
    # because we'll redefine open below (Python2)
    pyopen = open
elif open.__module__ == "io":
    # because we'll redefine open below (Python3)
    pyopen = open


def export(
    objectslist,
    filename
):
    "called when freecad exports a file"
    if len(objectslist) != 1:
        FreeCAD.Console.PrintError("This exporter can only export one object.\n")
        return
    obj = objectslist[0]
    if not obj.isDerivedFrom("Fem::FemMeshObject"):
        FreeCAD.Console.PrintError("No FEM mesh object selected.\n")
        return
    fem_mesh = obj.FemMesh
    f = pyopen(filename, "w")
    write_oofem_mesh_to_file(f, fem_mesh)
    f.close()


# ************************************************************************************************
# ********* module specific methods **************************************************************
# writer:
# - a method directly writes a FemMesh to the mesh file
# - a method takes a file handle, mesh data and writes to the file handle

# ********* writer *******************************************************************************
def write(
    fem_mesh,
    filename
):
    """directly write a FemMesh to a OOFEM mesh file format
    fem_mesh: a FemMesh"""

    if not fem_mesh.isDerivedFrom("Fem::FemMesh"):
        FreeCAD.Console.PrintError("Not a FemMesh was given as parameter.\n")
        return
    f = pyopen(filename, "w")
    write_oofem_mesh_to_file(f, fem_mesh)
    f.close()


def write_oofem_mesh_to_file(
    f,
    femmesh,
    femelement_table,
    mesh_ele_type=None
):
    """ *Node coords # (ra)
         [lcs # (ra) ]
        *ElementType
         (num#) (in)
         mat # (in) crossSect # (in) nodes # (ia)
         [bodyLoads # (ia) ] [boundaryLoads # (ia) ]
         [activityltf # (in) ] [lcs # (ra) ]
         [partitions # (ia) ] [remote]
             *beam2d
              2D beam element
              [dofstocondense # (ia) ]
             *beam3d
              3D beam element
              refnode # (in) [dofstocondense # (ia) ]
             *planestress2d
              4-noded 2D quadrilateral element for plane stress analysis
              [NIP # (in) ]
             *qplanestress2d
              8-noded 2D quadrilateral element for plane stress analysis
              [NIP # (in) ]
             *trplanestress2d
              3-noded 2D triangular element for plane stress analysis
             *qtrplstr
              6-noded 2D triangular element for plane stress analysis [NIP # (in) ]
             *quad1planestrain
              4-noded 2D quadrilateral element for plane strain analysis
              [NIP # (in) ]
             *trplanestrain
              3-noded 2D triangular element for plane strain analysis
             *lspace
              Linear 8-node isoparametric brick element
              [NIP # (in) ]
             *qspace
              Quadratic 20-node isoparametric brick element
              [NIP # (in) ]
             *LTRSpace
              Linear 4-node tetrahedra element
             *QTRSpace
              Quadratic 10-node tetrahedra element
              [NIP # (in) ]
    """

    if femelement_table is None:
        femelement_table = meshtools.get_femelement_table(femmesh)
    # mesh element type, mixed meshes not supported
    if mesh_ele_type is None:
        mesh_ele_type = get_mesh_ele_type(femmesh, femelement_table)
        print(mesh_ele_type)
    if mesh_ele_type is None:
        FreeCAD.Console.PrintError(
            "No FEM mesh element type. Mesh writing is not possible.\n"
        )
        return None

    # nodes
    f.write("# Node Records\n")
    f.write("#\n")
    node_dof = 3
    femnodes_mesh = femmesh.Nodes
    nodes_count = len(femmesh.Nodes)
    for node in femnodes_mesh:
        # nodes are NOT renumbered !!!
        vec = femnodes_mesh[node]
        """
        f.write(
            "node {0} coords {1}  {2:.6f}  {3:.6f}  {4:.6f}\n"
            .format(node, node_dof, vec.x, vec.y, vec.z)
        )
        """
        f.write(
            "node {0} coords {1}  {2}  {3}  {4}\n"
            .format(node, node_dof, vec.x, vec.y, vec.z)
        )

    # elements
    f.write("#\n")
    f.write("# Element Records\n")
    f.write("#\n")
    ele_count = 0
    for element in femelement_table:
        # elements are renumbered starting with 1 !!!
        # TODO probably check ele type for every element
        # or totally rewrite the writer independent from ele type
        # mesh_ele_type is NOT checked for every element
        # means on mixed meshes all elements are written with the same mesh_ele_type
        ele_count += 1
        n = femelement_table[element]
        if mesh_ele_type == "quad4":
            # quad8 FreeCAD --> PlaneStress2d OOFEM
            # N1, N2, N3, N4
            f.write(
                "PlaneStress2d {0} nodes 4  {1} {2} {3} {4}  NIP 1\n"
                .format(ele_count, n[0], n[1], n[2], n[3])
            )
            # whatever NIP 1 means, it is just from the example file
        elif mesh_ele_type == "tetra4":
            # tetra10 FreeCAD --> LTRSpace OOFEM
            # N1, N2, N4, N3, FC to OOFEM is different as OOFEM to FC
            f.write(
                "LTRSpace {0} nodes 4 {1} {2} {3} {4}\n"
                .format(ele_count, n[0], n[1], n[3], n[2])
            )
        elif mesh_ele_type == "tetra10":
            # tetra10 FreeCAD --> QTRSpace OOFEM
            # N1, N2, N4, N3, N5, N9, N8, N7, N6, N10, FC to OOFEM is different as OOFEM to FC
            f.write(
                "QTRSpace {0} nodes 10 {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n"
                .format(ele_count, n[0], n[1], n[3], n[2], n[4], n[8], n[7], n[6], n[5], n[9])
            )
        else:
            FreeCAD.Console.PrintError(
                "Writing of OOFEM elementtype {0} not supported.\n"
                .format(mesh_ele_type)
            )
            return None
    return (nodes_count, ele_count)


# Helper
def get_mesh_ele_type(femmesh, femelement_table=None):
    import femmesh.meshtools as meshtools
    if not femmesh:
        print("Error: No femmesh!")
    if not femelement_table:
        print("We need to get the femelement_table first!")
        femelement_table = meshtools.get_femelement_table(femmesh)
    # in some cases lowest key in femelement_table is not [1]
    for elem in sorted(femelement_table):
        elem_length = len(femelement_table[elem])
        # print(elem_length)
        break  # break after the first elem

    if meshtools.is_solid_femmesh(femmesh):
        if femmesh.TetraCount == femmesh.VolumeCount:
            if elem_length == 4:
                return "tetra4"
            elif elem_length == 10:
                return "tetra10"
            else:
                print("Tetra with neither 4 nor 10 nodes")
                return None
        elif femmesh.HexaCount == femmesh.VolumeCount:
            if elem_length == 8:
                return "hexa8"
            elif elem_length == 20:
                return "hexa20"
            else:
                print("Hexa with neither 8 nor 20 nodes")
                return None
        else:
            print("no tetra, no hexa or Mixed Volume Elements")
    elif meshtools.is_face_femmesh(femmesh):
        if femmesh.TriangleCount == femmesh.FaceCount:
            if elem_length == 3:
                return "tria3"
            elif elem_length == 6:
                return "tria6"
            else:
                print("Tria with neither 3 nor 6 nodes")
                return None
        elif femmesh.QuadrangleCount == femmesh.FaceCount:
            if elem_length == 4:
                return "quad4"
            elif elem_length == 8:
                return "quad8"
            else:
                print("Quad with neither 4 nor 8 nodes")
                return None
        else:
            print("no tria, no quad")
            return None
    elif meshtools.is_edge_femmesh(femmesh):
        print("Getting edge mesh types not supported ATM")
        return None
    return None
