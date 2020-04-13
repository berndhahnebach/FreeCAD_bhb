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
import os


__all__ = [
    'Steps',
]


class Steps(object):

    def __init__(self):

        pass

    def write_steps(self):

        self.write_section('Steps')
        self.blank_line()

        # Solver
        increments = 1
        paraview_output = "Paraview_Output"
        paraview_output_folder = os.path.join(self.dir_name, paraview_output)
        if not os.path.isdir(paraview_output_folder):
            os.mkdir(paraview_output_folder)

        self.blank_line()
        self.write_subsection("Solver")
        self.blank_line()

        self.write_line("system BandSPD")
        self.write_line("numberer RCM")
        self.write_line("constraints Plain")
        # self.write_line("test NormUnbalance {0} {1} 5".format(tolerance, iterations))
        self.write_line("integrator LoadControl {0}".format(1. / increments))
        self.write_line('algorithm Linear')
        self.write_line("analysis Static")
        self.write_line("recorder pvd {} disp reaction unbalancedLoad".format(paraview_output))
        self.write_line("analyze {0}".format(increments))
