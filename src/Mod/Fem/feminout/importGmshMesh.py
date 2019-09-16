# ***************************************************************************
# *   Copyright (c) 2017 Qingfeng Xia <qingfeng.xia@gmail.coom>             *
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
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

""" Methods to export a FemMesh to the file formats supported by Gmsh
see gmsh document object for the known gmsh output file formats

The export format has to be set in gmsh mesh object. There should be a switch
here which sets the export property in gmsh object or we make this an optional
parameter on instantiate the class of GmshTools or whatever.
If the user exports to msh Init.py will call the export method here, 
but if in gmsh mesh object the export property is set to ply2 the
mesh is exported to ply2. This should not happen.

Or the other way around, if export format has changed per accident
the solver execution does not work anymore because input file writing
would be broken. This should not happen.

Furthermore, stl, inp, unv can be chosen as well, thus they might also
be in init, but if chosen to use gmsh to export them we need to make
sure the file was exported by the use of gmsh.

Furthermore if a mesh is just exported to stl or inp by python which
exporter is taken? This should be clear without having to look
into the source.

There are some things left to tackle.

forum topic: 
https://forum.freecadweb.org/viewtopic.php?t=23702

old PR for FreeCAD:
https://github.com/FreeCAD/FreeCAD/pull/931

original dev repo from qingfengxia:
https://github.com/qingfengxia/FreeCAD/commits/gmshoutput

rebased by bernd
https://github.com/berndhahnebach/FreeCAD_bhb/commits/femgmshexport

"""

__title__ = "FreeCAD Gmsh supported format mesh export"
__author__ = "Qingfeng Xia, Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"

## @package importGmshMesh
#  \ingroup FEM
#  \brief gmsh supported format mesh export from FemMeshGmsh object

import os
import os.path
import subprocess
import sys

import FreeCAD

import FemGui
from femmesh import gmshtools
from femtools import femutils


if sys.version_info.major >= 3:
    unicode = str


# ************************************************************************************************
# ********* generic FreeCAD import and export methods ********************************************
# only export is supported, thus neither open nor insert method is needed

# boundary mesh might also be exported

def export(objectslist, fileString):
    """called when freecad exports a mesh file supprted by gmsh generation
    """
    if len(objectslist) != 1:
        FreeCAD.Console.PrintError("This exporter can only export one object.\n")
        return
    obj = objectslist[0]
    if not obj.isDerivedFrom("Fem::FemMeshObject"):
        FreeCAD.Console.PrintError("No FEM mesh object selected.\n")
        return
    if not femutils.is_of_type(obj, "Fem::FemMeshGmsh"):
        FreeCAD.Console.PrintError("Object selected is not a FemMeshGmsh type\n")
        return

    if FreeCAD.GuiUp:
        import FemGui
        analysis = FemGui.getActiveAnalysis()
        gmsh = gmshtools.GmshTools(obj, analysis)
    else:
        # it is still possible to lookup analysis object from document
        gmsh = gmshtools.GmshTools(obj)
    if fileString != "":
        fileName, fileExtension = os.path.splitext(fileString)
        for k in gmshtools.GmshTools.output_format_suffix:
            if gmshtools.GmshTools.output_format_suffix[k] == fileExtension.lower():
                ret = gmsh.export_mesh(k, fileString)
                if not ret:
                    FreeCAD.Console.PrintError("Mesh is written to `{}` by Gmsh\n".format(ret))
                return
        FreeCAD.Console.PrintError(
            "Export mesh format with suffix `{}` is not supported by Gmsh\n"
            .format(fileExtension.lower())
        )


# ************************************************************************************************
# ********* module specific methods **************************************************************

# none
