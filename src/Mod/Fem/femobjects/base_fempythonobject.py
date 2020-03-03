# ***************************************************************************
# *   Copyright (c) 2017 Markus Hovorka <m.hovorka@live.de>                 *
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

__title__ = "FreeCAD FEM base python object"
__author__ = "Markus Hovorka, Bernd Hahnebach"
__url__ = "https://www.freecadweb.org"

## @package base_fempythonobject
#  \ingroup FEM
#  \brief base object for FEM Python Features

# some information:
# in FemConstraint add a link to Yoriks explanation about the type
# https://forum.freecadweb.org/viewtopic.php?t=38820#p329408
# https://forum.freecadweb.org/viewtopic.php?t=26126
# https://forum.freecadweb.org/viewtopic.php?f=10&t=42948
# Proxy.Type will not be written into saved document but module and class name will
# all Python obj. use Fem::Name not Fem::FemName
# C++ obj use a mix some are with some without second Fem

# classes inherited from FemConstraint usually have the class name class Proxy
# for compativility reason some classes newly changed to inherit from
# FemConstraint are kept because of compativility reason
# if class name of a object changes it will not be proper loaded anymore
# because class names and module names are written into document
# this is needed for object rebuild on document reload

# all could be named Proxy and for reading the old one an inherited class which
# inits the Proxi one should be ok

# no init in inherited class ... only the methods from base class will be inherited
# init in inherited class which calls init of base clase, this will be run
# and may be some attributes are added
# any other class from base class could be called too, see setEdit in VP classes


class BaseFemPythonObject(object):

    BaseType = "Fem::BaseFemPythonObject"

    def __init__(self, obj):
        # self.Object = obj  # keep a ref to the DocObj for nonGui usage
        obj.Proxy = self  # link between App::DocumentObject to this object

    # they are needed, see:
    # https://forum.freecadweb.org/viewtopic.php?f=18&t=44021
    # https://forum.freecadweb.org/viewtopic.php?f=18&t=44009
    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
