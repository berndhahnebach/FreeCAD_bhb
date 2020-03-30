# ***************************************************************************
# *   Copyright (c) 2018 Bernd Hahnebach <bernd@bimstatik.org>              *
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

__title__ = "Solver OOFEM unit tests"
__author__ = "Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"

import unittest
from os.path import join

import FreeCAD

from . import support_utils as testtools
from .support_utils import fcc_print
from .support_utils import get_namefromdef


class TestSolverOofem(unittest.TestCase):
    fcc_print("import TestSolverOofem")

    # ********************************************************************************************
    def setUp(
        self
    ):
        # setUp is executed before every test

        # new document
        self.document = FreeCAD.newDocument(self.__class__.__name__)

        # more inits
        self.mesh_name = "Mesh"
        self.temp_dir = testtools.get_fem_test_tmp_dir()
        self.test_file_dir = join(
            testtools.get_fem_test_home_dir(),
            "oofem"
        )

    # ********************************************************************************************
    def tearDown(
        self
    ):
        # tearDown is executed after every test
        FreeCAD.closeDocument(self.document.Name)

    # ********************************************************************************************
    def test_planestress2d(
        self
    ):
        from femexamples.oofem_planestress2d import setup
        setup(self.document, "oofem")
        self.input_file_writing_test(get_namefromdef("test_"))

    # ********************************************************************************************
    def test_ccxcantilever_nodeload(
        self
    ):
        from femexamples.ccx_cantilever_nodeload import setup
        setup(self.document, "oofem")
        self.input_file_writing_test(get_namefromdef("test_"))

    # ********************************************************************************************
    def test_ccxcantilever_prescribeddisplacement(
        self
    ):
        from femexamples.ccx_cantilever_prescribeddisplacement import setup
        setup(self.document, "oofem")
        self.input_file_writing_test(get_namefromdef("test_"))

    # ********************************************************************************************
    def input_file_writing_test(
        self,
        base_name
    ):

        # recompute
        self.document.recompute()

        # fcc_print(self.document.Objects)
        # fcc_print([obj.Name for obj in self.document.Objects])

        # save file, needs before input file writing because of besides dir
        solverframework_analysis_dir = testtools.get_unit_test_tmp_dir(
            testtools.get_fem_test_tmp_dir(),
            "FEM_oofem"
        )
        save_fc_file = join(solverframework_analysis_dir, base_name) + ".FCStd"
        fcc_print(
            "Save FreeCAD file for {} analysis to {}"
            .format(base_name, save_fc_file)
        )
        self.document.saveAs(save_fc_file)

        # solver
        solver = self.document.SolverOOFEM

        # get analysis workig dir
        from femtools.femutils import get_beside_dir
        working_dir = get_beside_dir(solver)

        fcc_print("Checking FEM OOFEM solver ...")
        fcc_print("machine_oofem")

        # write input file
        from femsolver.run import PREPARE
        # set up the machine with testmode True
        machine_oofem = solver.Proxy.createMachine(solver, working_dir, True)
        machine_oofem.target = PREPARE
        machine_oofem.start()
        machine_oofem.join()  # wait for the machine to finish.

        # compare input files
        inpfile_given = join(
            testtools.get_fem_test_home_dir(),
            "oofem",
            (base_name + ".in")
        )
        inpfile_totest = join(
            working_dir,
            (self.mesh_name + ".in")
        )
        fcc_print(
            "Comparing {}  to  {}"
            .format(inpfile_given, inpfile_totest)
        )
        ret = testtools.compare_inp_files(
            inpfile_given,
            inpfile_totest
        )
        self.assertFalse(
            ret,
            "OOFEM write_inp_file for {0} test failed.\n{1}".format(base_name, ret)
        )
