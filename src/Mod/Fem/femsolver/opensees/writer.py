# ***************************************************************************
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
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

"""
# set up test file in FreeCAD Gui
from femexamples import ccx_cantilever_std as canti
canti.setup_cantileverhexa20faceload(solvertype="opensees")

# run OpenSees solver
from femsolver.run import run_fem_solver as run
run(App.ActiveDocument.SolverOpenSees)

"""

__title__ = "OpenSees Writer"
__author__ = "Bernd Hahnebach, Raeyat Roknabadi Ebrahim"
__url__ = "http://www.freecadweb.org"

## \addtogroup FEM
#  @{

from os.path import join

import FreeCAD

from .bcs import BCs
from .elements import Elements
from .heading import Heading
from .loads import Loads
from .materials import Materials
from .nodes import Nodes
# from .sets import Sets
from .steps import Steps
from .. import writerbase
from femmesh import meshtools


__all__ = [
    'FemInputWriterOpenSees',
]


comments = {
    'abaqus': '**',
    'opensees': '#',
    'sofistik': '$',
    'ansys': '!',
}


class FemInputWriterOpenSees(writerbase.FemInputWriter,
                             Steps,
                             BCs,
                             # Sets,
                             Loads,
                             Materials,
                             Elements,
                             Nodes,
                             Heading):

    """ Initialises base file writer.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    def __init__(self,
                 analysis_obj,
                 solver_obj,
                 mesh_obj,
                 member,
                 dir_name=None,
                 structure=None,
                 software='opensees',
                 filename='/home/ebi/freecad_opensees.tcl',
                 fields=None,
                 ndof=6,
                 ):
        writerbase.FemInputWriter.__init__(self,
                                           analysis_obj,
                                           solver_obj,
                                           mesh_obj,
                                           member,
                                           dir_name,
                                           )

        self.comment = comments[software]
        self.file_name = join(self.dir_name, self.mesh_object.Name + ".tcl")
        self.member = member
        self.ndof = ndof
        self.software = software
        self.structure = structure
        self.fields = fields
        self.spacer = {'abaqus': ', ', 'opensees': ' ', 'ansys': ' '}

    def write_opensees_input_file(self):

        if not self.femnodes_mesh:
            self.femnodes_mesh = self.femmesh.Nodes
        if not self.femelement_table:
            self.femelement_table = meshtools.get_femelement_table(self.femmesh)
            self.element_count = len(self.femelement_table)
        self.get_constraints_force_nodeloads()
        self.get_element_sets_material_and_femelement_type()

        self.write_heading()
        self.write_materials()
        self.write_nodes()
        self.write_boundary_conditions()
        self.write_elements()
        self.write_loads()
        self.write_steps()

        print('***** OpenSees input file generated: {0} *****\n'.format(self.file_name))
        return self.file_name

    def __enter__(self):

        self.file = open(self.file_name, 'w')
        return self

    def __exit__(self, type, value, traceback):

        self.file.close()

    def blank_line(self):

        self.file.write('{0}\n'.format(self.comment))

    def divider_line(self):

        self.file.write('{0}'.format(self.comment) + 65 * '-' + '\n')

    def write_line(self, line):

        self.file.write('{0}\n'.format(line))

    def write_section(self, section):

        self.divider_line()
        self.write_line('{0} {1}'.format(self.comment, section))
        self.divider_line()

    def write_subsection(self, subsection):

        self.write_line('{0} {1}'.format(self.comment, subsection))
        self.write_line('{0}-{1}'.format(self.comment, '-' * len(subsection)))
        self.blank_line()
##  @}
