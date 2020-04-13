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

from math import pi
import FreeCAD


__all__ = [
    'Elements',
]


class Elements(object):

    def __init__(self):

        pass

    @staticmethod
    def element_1D_ifcType(p1, p2):
        normal = abs(p2 - p1)
        if normal.z > max(normal.x, normal.y):
            # column
            return "PDelta"
        else:
            # beam
            return "Linear"

    def write_elements(self):

        self.write_section('Elements')
        self.blank_line()
        print(self.ccx_elsets)

        # print(f"self.beamsection_objects = {self.beamsection_objects}")
        # print(f"self.transform_objects = {self.transform_objects}")
        # print(f"self.material_objects = {self.material_objects}")

        for ccx_elset in self.ccx_elsets:
            if ccx_elset["ccx_elset"]:
                if "beamsection_obj"in ccx_elset:  # beam mesh
                    e = 'element elasticBeamColumn'
                    beamsec_obj = ccx_elset["beamsection_obj"]
                    A = beamsec_obj.Area
                    J = beamsec_obj.J
                    Izz = beamsec_obj.Izz
                    Iyy = beamsec_obj.Iyy
                    E = 200000
                    G = 1000
                    normal = ccx_elset["beam_normal"]
                    # beamsec_obj = ccx_elset["beamsection_obj"]
                    # elsetdef = "ELSET=" + ccx_elset["ccx_elset_name"] + ", "
                    # material = "MATERIAL=" + ccx_elset["mat_obj_name"]

                    # if beamsec_obj.SectionType == "Rectangular":
                    #     height = beamsec_obj.RectHeight.getValueAs("mm")
                    #     width = beamsec_obj.RectWidth.getValueAs("mm")
                    #     section_type = ", SECTION=RECT"
                    #     section_geo = str(height) + ", " + str(width) + "\n"
                    #     section_def = "*BEAM SECTION, {}{}{}\n".format(
                    #         elsetdef,
                    #         material,
                    #         section_type
                    #     )
                    # elif beamsec_obj.SectionType == "Circular":
                    #     radius = 0.5 * beamsec_obj.CircDiameter.getValueAs("mm")
                    #     section_type = ", SECTION=CIRC"
                    #     section_geo = str(radius) + "\n"
                    #     section_def = "*BEAM SECTION, {}{}{}\n".format(
                    #         elsetdef,
                    #         material,
                    #         section_type
                    #     )
                    # elif beamsec_obj.SectionType == "Pipe":
                    #     radius = 0.5 * beamsec_obj.PipeDiameter.getValueAs("mm")
                    #     thickness = beamsec_obj.PipeThickness.getValueAs("mm")
                    #     section_type = ", SECTION=PIPE"
                    #     section_geo = str(radius) + ", " + str(thickness) + "\n"
                    #     section_def = "*BEAM GENERAL SECTION, {}{}{}\n".format(
                    #         elsetdef,
                    #         material,
                    #         section_type
                    #     )

                    for ele_id in ccx_elset["ccx_elset"]:
                        nodes = self.femelement_table[ele_id]
                        if len(nodes) == 3:
                            self.write_line("remove node {}".format(nodes[2]))
                        p1 = self.femnodes_mesh[nodes[0]]
                        p2 = self.femnodes_mesh[nodes[1]]
                        geomtransf = Elements.element_1D_ifcType(p1, p2)
                        self.write_line('geomTransf {0} {1} {2}'.format(geomtransf, ele_id, ' '.join([str(i) for i in normal])))

                        self.write_line("{} {} {} {} {} {} {} {} {} {} {}".format(e, ele_id, nodes[0], nodes[1], A, E, G, J, Izz, Iyy, ele_id))

            # self.write_subsection(key)

            # property      = properties[key]
            # reinforcement = property.rebar
            # elset         = property.elset

            # section       = sections[property.section]
            # stype         = section.__name__
            # geometry      = section.geometry
            # material      = materials.get(property.material)

            # if material:
            #     m_index = material.index + 1

            # s_index = section.index + 1

            # selection = property.elements if property.elements else sets[elset].selection

            # if geometry is not None:

            #     t   = geometry.get('t', None)

            # elif n == 4:
            #     e = 'element ShellMITC4'
            # elif n == 20:
            #     e = 'element 20NodeBrick'
            #     # rearrange nodes number to avoid negative jacobian
            #     maps = [6, 7, 8, 5, 2, 3, 4, 1, 14, 15, 16, 13, 10, 11, 12, 9, 18, 19, 20, 17]
            #     nodes = ''.join(f"{nodes[i - 1]} " for i in maps)
            #     self.write_line('{0} {1} {2} {3}'.format(e, key, nodes, 1))
            # else:
            #     FreeCAD.Console.PrintError(
            #         "Writing of OpenSees {} Nodes element not supported.\n".format(len(nodes)))
            # self.write_line('element {0} {1} {2} {3}'.format(solid, key, nodes, 1))

            # =====================================================================================================
            # =====================================================================================================
            # SHELL
            # =====================================================================================================
            # =====================================================================================================

            # if no == 3:
            #     self.write_line('element tri31 {0} {1} {2} PlaneStress {3} 0 {4} 0 0'.format(
            #                     n, ' '.join(nodes), t, m_index + 1000, material.p))
                # self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
                # self.write_line('element ShellDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                # self.write_line('element ShellNLDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                # apparently unknown to OpenSees
            # else:
            #     self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
            #     self.write_line('element ShellNLDKGQ {0} {1} {0}'.format(n, ' '.join(nodes)))

            # elif stype == 'TrussSection':

            #     e = 'element corotTruss'
            #     self.write_line('{0} {1} {2} {3} {4} {5}'.format(
            #         e, n, nodes[0], nodes[1], A, m_index))

            # elif stype == 'SpringSection':

            #     kx = section.stiffness.get('axial', 0)
            #     ky = section.stiffness.get('lateral', 0)
            #     kr = section.stiffness.get('rotation', 0)

            #     if s_index not in written_springs:

            #         if kx:

            #             self.write_line('uniaxialMaterial Elastic 2{0:0>3} {1}'.format(
            # s_index, kx))
            #             self.blank_line()

            #         # else:
            #         #     i = ' '.join([str(k) for k in section.forces['axial']])
            #         #     j = ' '.join([str(k) for k in section.displacements['axial']])
            #         #     f.write('uniaxialMaterial ElasticMultiLinear {0}01
            #         # -strain {1} -stress {2}\n'.format(
            #         #         s_index, j, i))
            #         #     f.write('#\n')

            #         written_springs.append(s_index)

            #     orientation = ' '.join([str(k) for k in ey])

            #     self.write_line('element twoNodeLink {0} {1} {2}
            # -mat 2{3:0>3} -dir 1 -orient {4}'.format(
            #         n, nodes[0], nodes[1], s_index, orientation))

        self.blank_line()
        self.blank_line()


# def _write_membranes(elements, geometry, material, materials, reinforcement):

#     for select in selection:

#         element = elements[select]
#         nodes   = element.nodes
#         n  = select + 1
#         t  = geometry['t']
#         ex = element.axes.get('ex', None)
#         ey = element.axes.get('ey', None)

#         if software == 'abaqus':

#             e1 = 'element_{0}'.format(select)
#             f.write('*ELEMENT, TYPE={0}, ELSET={1}\n'.format(
# 'M3D3' if len(nodes) == 3 else 'M3D4', e1))
#             f.write('{0}, {1}\n'.format(n, ','.join([str(i + 1) for i in nodes])))

#             if ex and ey:
#                 ori = 'ORI_element_{0}'.format(select)
#                 f.write('*ORIENTATION, NAME={0}\n'.format(ori))
#                 f.write(', '.join([str(j) for j in ex]) + ', ')
#                 f.write(', '.join([str(j) for j in ey]) + '\n')
#                 f.write('**\n')
#             else:
#                 ori = None

#             f.write('*MEMBRANE SECTION, ELSET={0}, MATERIAL={1}'.format(e1, material.name))
#             if ori:
#                 f.write(', ORIENTATION={0}\n'.format(ori))
#             else:
#                 f.write('\n'.format(t))
#             f.write('{0}\n'.format(t))

#         f.write('{0}\n'.format(comments[software]))
