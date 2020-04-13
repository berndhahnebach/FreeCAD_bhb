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
    'Loads',
]


class Loads(object):

    def __init__(self):

        pass

    def write_loads(self):

        self.write_section('Loads')
        self.blank_line()

        for femobj in self.force_objects:
            # femobj --> dict, FreeCAD document object is femobj["Object"]
            direction_vec = femobj["Object"].DirectionVector
            for ref_shape in femobj["NodeLoadTable"]:
                self.write_line("pattern Plain 1 Linear {")
                for n in sorted(ref_shape[1]):
                    node_load = ref_shape[1][n]
                    v1 = direction_vec.x * node_load
                    v2 = direction_vec.y * node_load
                    v3 = direction_vec.z * node_load
                    ltype = "PointLoad"

                    # PointLoad
                    # ---------

                    if ltype == 'PointLoad':

                        self.write_line('\tload {0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t0\t0\t0'.format(
                            n, v1, v2, v3))

                    # Gravity
                    # -------

                    # elif ltype == 'GravityLoad':

                    #     for nkey, node in self.structure.nodes.items():

                    #         W = - fact * node.mass * 9.81
                    #         self.write_line('load {0}\t{1:.3f}\t{2:.3f}\t{3:.3f}'.format(
                    # nkey + 1, gx * W, gy * W, gz * W))

                    # # LineLoad
                    # # --------

                    # elif ltype == 'LineLoad':

                    #     if axes == 'global':

                    #         raise NotImplementedError

                    #     elif axes == 'local':

                    #         elements = ' '.join([str(i + 1) for i in sets[k].selection])
                    #         lx = -com['x'] * fact
                    #         ly = -com['y'] * fact
                    #         self.write_line('eleLoad -ele {0} -type -\
                    # beamUniform {1} {2}'.format(elements, ly, lx))

                self.write_line("}")

                self.blank_line()
                self.blank_line()
