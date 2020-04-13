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

import FreeCAD


__all__ = [
    'Materials',
]


class Materials(object):

    def __init__(self):

        pass

    def write_materials(self):

        self.write_section('Materials')
        self.blank_line()
        mat_obj = self.material_objects[0]["Object"]
        E = FreeCAD.Units.Quantity(mat_obj.Material["YoungsModulus"])
        E = E.getValueAs("kg/(mm*s^2)")
        v = float(mat_obj.Material["PoissonRatio"])
        p = FreeCAD.Units.Quantity(mat_obj.Material["Density"])
        p = p.getValueAs("kg/mm^3")

        mtype = 'ElasticIsotropic'

        # Elastic
        # -------

        if mtype == 'ElasticIsotropic':

            # self.write_line('uniaxialMaterial Elastic {0} {1}'.format(m_index, E['E']))
            self.write_line('nDMaterial ElasticIsotropic {0} {1} {2} {3}'.format(
                            1, E.Value, v, p.Value))

        # elif mtype == 'Steel':

        #     fy = material.fy
        #     fu = material.fu
        #     ep = material.ep
        #     EshE = (fu - fy) / ep

        #     self.write_line('uniaxialMaterial Steel01 {0} {1} {2} {3}'.format(
        #         m_index, fy, E['E'], EshE))

        self.blank_line()
        self.blank_line()


# f.write('*CONDUCTIVITY\n')
# f.write('** k[W/mK]\n')
# f.write('**\n')

# for i in material.conductivity:
#     f.write(', '.join([str(j) for j in i]) + '\n')

# f.write('**\n')
# f.write('*SPECIFIC HEAT\n')
# f.write('** c[J/kgK]\n')
# f.write('**\n')

# for i in material.sheat:
#     f.write(', '.join([str(j) for j in i]) + '\n')
