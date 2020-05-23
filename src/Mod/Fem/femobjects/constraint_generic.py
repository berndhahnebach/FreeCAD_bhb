# ***************************************************************************
# *   Copyright (c) 2018 qingfeng Xia <qingfeng.xia@gmail.coom>             *
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

__title__ = "FreeCAD FEM constraint body (point, line, face, volume) source document object"
__author__ = "Bernd Hahnebach, Qingfeng Xia"
__url__ = "http://www.freecadweb.org"

## @package _FemConstraintGeneric
#  \ingroup FEM
#  \brief FreeCAD FEM generic constraint object

from . import base_fempythonobject


class ConstraintGeneric(base_fempythonobject.BaseFemPythonObject):
    """
    The generic object for initial values and body source FemConstraint
    """

    Type = "Fem::ConstraintGeneric"

    def __init__(self, obj):
        super(ConstraintGeneric, self).__init__(obj)

        obj.addProperty(
            "App::PropertyEnumeration",
            "Category",
            "GenericConstraint",
            "to distinguish constraint or initial value or source"
        )
        obj.addProperty(
            "App::PropertyLinkSubList",
            "References", "GenericConstraint",
            "List of geometry references/links"
        )
        obj.addProperty(
            "App::PropertyEnumeration",
            "ShapeType",  # code review: rename to PreferedShapeType or DefaultShapeType
            "GenericConstraint",
            "the default geometry shape type for this constraint"
        )
        obj.addProperty(
            "App::PropertyStringList",
            "ShapeTypes",
            "GenericConstraint",
            "List of applicable shape types"
        )
        obj.addProperty(
            "App::PropertyPythonObject",
            "Settings",
            "GenericConstraint",
            "A dictionary holds settings for constraint, initial value or source"
        )
        obj.Category = ["Constraint", "InitialValue", "Source"]
        obj.Category = "Constraint"
        obj.ShapeTypes = ["Solid", "Face", "Edge", "Vertex"]  # == OCCT ShapeType names
        obj.ShapeType = ["Solid", "Face", "Edge", "Vertex"]  # == OCCT ShapeType names
        obj.ShapeType = "Solid"  # default shape type
        obj.References = []
        obj.Settings = {"Velocity": {}}
