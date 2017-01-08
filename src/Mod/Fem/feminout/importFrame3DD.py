# ***************************************************************************
# *   Copyright (c) 2017 Bernd Hahnebach <bernd@bimstatik.org>              *
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

__title__ = "FreeCAD Frame3DD Mesh reader and writer"
__author__ = "Bernd Hahnebach "
__url__ = "http://www.freecadweb.org"

## @package importFrame3DD
#  \ingroup FEM

import FreeCAD
import os
import FemMeshTools


Debug = False


"""
https://forum.freecadweb.org/viewtopic.php?t=19428
https://forum.freecadweb.org/viewtopic.php?t=43386
https://forum.freecadweb.org/viewtopic.php?t=43389
https://forum.freecadweb.org/viewtopic.php?t=45026
"""


# ********* generic FreeCAD import and export methods *********
if open.__module__ == '__builtin__':
    pyopen = open  # because we'll redefine open below


def open(filename):
    "called when freecad opens a file"
    docname = os.path.splitext(os.path.basename(filename))[0]
    insert(filename, docname)


def insert(filename, docname):
    "called when freecad wants to import a file"
    try:
        doc = FreeCAD.getDocument(docname)
    except NameError:
        doc = FreeCAD.newDocument(docname)
    FreeCAD.ActiveDocument = doc
    import_frame3dd_mesh(filename)


def export(objectslist, filename):
    "called when freecad exports a file"
    if len(objectslist) != 1:
        FreeCAD.Console.PrintError("This exporter can only export one object.\n")
        return
    obj = objectslist[0]
    if not obj.isDerivedFrom("Fem::FemMeshObject"):
        FreeCAD.Console.PrintError("No FEM mesh object selected.\n")
        return
    femnodes_mesh = obj.FemMesh.Nodes
    femelement_table = FemMeshTools.get_femelement_table(obj.FemMesh)
    f = pyopen(filename, "wb")
    write_frame3dd_mesh_to_file(femnodes_mesh, femelement_table, f)
    f.close()


# ********* module specific methods *********
# import Frame3DD Mesh
def import_frame3dd_mesh(filename, analysis=None):
    '''insert a FreeCAD FEM Mesh object in the ActiveDocument
    '''
    mesh_data = read_frame3dd_mesh(filename)
    mesh_name = os.path.basename(os.path.splitext(filename)[0])
    femmesh = FemMeshTools.make_femmesh(mesh_data)
    if femmesh:
        mesh_object = FreeCAD.ActiveDocument.addObject('Fem::FemMeshObject', mesh_name)
        mesh_object.FemMesh = femmesh


def read_frame3dd_mesh(frame3dd_mesh_input):
    ''' reads a Frame3DD mesh file *.3dd
        and extracts the nodes and elements
    '''
    nodes = {}
    elements_seg2 = {}

    frame3dd_mesh_file = pyopen(frame3dd_mesh_input, "r")
    # mesh_info = frame3dd_mesh_file.readline().strip().split()

    frame3dd_mesh_file.close()
    return {'Nodes': nodes, 'Seg2Elem': elements_seg2,
            }


# export Frame3DD Mesh
def write_frame3dd_mesh_to_file(femnodes_mesh, femelement_table, f):
    # node_dimension = 3  # 2 for 2D not supported
    node_count = len(femnodes_mesh)
    node_fixes = 0
    # element_count = len(femelement_table)
    information = "Frame3DD export, written by FreeCAD (N,mm)"

    # some information at file begin
    f.write("{0}\n".format(information))
    f.write("\n")

    # node data
    f.write("# node data ...\n")
    f.write("{0}     # number of nodes\n".format(node_count))
    f.write("# node   x    y    z   r\n")
    for node in femnodes_mesh:
        vec = femnodes_mesh[node]
        f.write("{0}  {1:.6f}  {2:.6f}  {3:.6f}  0.0\n".format(node, vec.x, vec.y, vec.z))

    f.write("\n")
    f.write("{0}     # number of nodes with reactions\n".format(node_fixes))
    f.write("# node     x  y  z xx yy zz          1=fixed, 0=free\n")

    # elements data
    for element in femelement_table:
        pass
