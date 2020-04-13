# ***************************************************************************
# *   Copyright (c) 2020 Raeyat Roknabadi Ebrahim <ebe79442114@gmail.com>   *
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


__all__ = [
    'BCs',
]


class BCs(object):

    def __init__(self):

        pass

    def write_boundary_conditions(self):

        self.get_constraints_fixed_nodes()
        self.write_section('Boundary conditions')
        self.blank_line()

        entry = '1 1 1 1 1 1'

        for femobj in self.fixed_objects:
            # femobj --> dict, FreeCAD document object is femobj["Object"]
            fix_obj = femobj["Object"]
            if self.femmesh.Volumes \
                    and (len(self.shellthickness_objects) > 0 or len(self.beamsection_objects) > 0):
                if len(femobj["NodesSolid"]) > 0:
                    self.write_line("#NSET,NSET=" + fix_obj.Name + "Solid")
                    for n in femobj["NodesSolid"]:
                        self.write_line("fix {0} {1}".format(n, " ".join(entry)))
                if len(femobj["NodesFaceEdge"]) > 0:
                    self.write_line("#NSET,NSET=" + fix_obj.Name + "FaceEdge")
                    for n in femobj["NodesFaceEdge"]:
                        self.write_line("fix {0} {1}".format(n, " ".join(entry)))
            else:
                self.write_line("#NSET,NSET=" + fix_obj.Name)
                for n in sorted(femobj["Nodes"], key=int):
                    self.write_line("fix {0} {1}".format(n, " ".join(entry)))

        self.blank_line()
        self.blank_line()
