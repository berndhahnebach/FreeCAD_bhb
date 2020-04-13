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
    'Nodes',
]


class Nodes(object):

    def __init__(self):
        pass

    def write_nodes(self):

        header = {
            'abaqus': '**\n*NODE, NSET=nset_all\n**',
            'opensees': '#',
            'ansys': '!',
        }

        self.prefix = {
            'abaqus': '',
            'opensees': 'node ',
            'ansys': '',
        }

        self.write_section('Nodes')
        self.write_line(header[self.software])

        for key in sorted(self.femnodes_mesh, key=int):

            self.write_node(key)

        # if self.software == 'opensees':
        #     self.blank_line()
        #     for key in sorted(self.structure.nodes, key=int):
        #         if self.structure.nodes[key].mass:
        #             self.write_mass(key)

        self.blank_line()
        self.blank_line()

    def write_node(self, key):

        prefix = self.prefix[self.software]
        spacer = self.spacer[self.software]
        vector = self.femnodes_mesh[key]
        x, y, z = vector.x, vector.y, vector.z

        line = '{0}{1}{2}{3:.3f}{2}{4:.3f}{2}{5:.3f}'.format(prefix, key, spacer, x, y, z)
        self.write_line(line)

    def write_mass(self, key):

        mr = '' if self.ndof == 3 else '0 0 0'
        line = 'mass {0} {1} {1} {1} {2}'.format(key + 1, self.structure.nodes[key].mass, mr)
        self.write_line(line)
