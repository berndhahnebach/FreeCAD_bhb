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

## @package ConstraintGenericDefaults
#  \ingroup FEM
#  \brief FreeCAD FEM generic constraint object defaults


# more information
# https://forum.freecadweb.org/viewtopic.php?f=18&t=33124

# this constraint could replace:
#     constraint body heat source
#     constraint self weight (gravity is kind of BodyAcceleration)
#     constraint initial temperature
#     constraint initial flow velocity
# ATM the new ones are not implemented in any writer
# this has to be done before any other constraint could be declared deprecated
# Furthermore some converter needs to be implemented


# first commit: generic objects, here the _make methods only
#               they should be at module top
# second commit: icons, no command, because the generic obj itself has no command
# further commits: for each constraint based on the new generic ones, one commit


# it would be good to be able to add such a generic obj too and decide
# at runtime about the attributes, TODO for later


# no matter how the generic constraint is implemented.
# each constraint should have
# - its command name and class in command module, thus its icon
# - its make method here

# but may be this all makes sense only for constraints implemented on run time
# by external macros and workbenches

# for internal FEM constraints hard coded FreeCAD attributes and property editor
# seams more robust to me


# where is the best place to put these constants?
# for all other constraints attribute definition is in class in femobjects
# means these should be in femobjects too
# - here in _FemGenericConstraint
# - in one separate module in femobjects
# - one module for each constraint based on the generic one. Just one dict per module?
# - or one module for all initial values and one for body source


_DefaultConstraintAcceleration = {
    "Name": "Acceleration",
    "Symbol": u"g",
    "ValueType": "Quantity",
    "NumberOfComponents": 3,
    "Unit": "m/s^2",
    "Value": [0, 0, -9.8]
}
_DefaultConstraintInitialPressure = {
    "Name": "Pressure",
    "Symbol": u"p",
    "ValueType": "Expression",
    "NumberOfComponents": 1,
    "Unit": "MPa",
    "Value": "0.1"
}
"""
_DefaultInitialTemperature = {
    "Name": "Temperature",
    "Symbol": u"T",
    "ValueType": "Quantity",
    "NumberOfComponents": 1,
    "Unit": "K",
    "Value": 300
}
"""
