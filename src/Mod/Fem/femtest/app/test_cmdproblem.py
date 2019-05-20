# ***************************************************************************
# *   Copyright (c) 2019 - FreeCAD Developers                               *
# *   Author: Bernd Hahnebach <bernd@bimstatik.org>                         *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

import Part
import Fem
import FreeCAD
import ObjectsFem
import unittest
from . import support_utils as testtools
from .support_utils import fcc_print

from os.path import join


class TestCmdProblem(unittest.TestCase):
    fcc_print('import TestCmdProblem')

    def setUp(self):
        # init, is executed before every test
        self.doc_name = "TestCmdProblem"
        try:
            FreeCAD.setActiveDocument(self.doc_name)
        except:
            FreeCAD.newDocument(self.doc_name)
        finally:
            FreeCAD.setActiveDocument(self.doc_name)
        self.active_doc = FreeCAD.ActiveDocument

    def test_cmdproblem(self):
        box = self.active_doc.addObject(
            "Part::Box",
            "Box"
        )
        fixed_constraint = self.active_doc.addObject(
            "Fem::ConstraintFixed",
            "FemConstraintFixed"
        )
        fixed_constraint.References = [(box, "Face1")]
        self.active_doc.recompute()

        ref = fixed_constraint.References[0]
        femmesh = Fem.FemMesh()

        from femmesh.meshtools import get_femnodes_by_refshape as getnodes
        getnodes(femmesh, ref)

    def test_face_subclass1(self):

        box=Part.makeBox(1,1,1)
        fcc_print('\n')
        fcc_print('Shape: {}'.format(box))
        fcc_print('ShapeType: {}'.format(box.ShapeType))
        face = box.Face1
        fcc_print('Subclass: {}'.format(issubclass(type(face), Part.Face)))

    def test_face_subclass2(self):

        box = self.active_doc.addObject(
            "Part::Box",
            "Box"
        )
        fcc_print('\n')
        fcc_print('Shape: {}'.format(box.Shape))
        fcc_print('isNull: {}'.format(box.Shape.isNull()))
        self.active_doc.recompute()
        fcc_print('\n')
        fcc_print('Shape: {}'.format(box.Shape))
        fcc_print('isNull: {}'.format(box.Shape.isNull()))
        fcc_print('ShapeType: {}'.format(box.Shape.ShapeType))
        face = box.Shape.Face1
        fcc_print('Subclass: {}'.format(issubclass(type(face), Part.Face)))

        fixed_constraint = self.active_doc.addObject(
            "Fem::ConstraintFixed",
            "FemConstraintFixed"
        )
        fixed_constraint.References = [(box, "Face1")]
        self.active_doc.recompute()

        ref = fixed_constraint.References[0]
        femmesh = Fem.FemMesh()

        from femmesh.meshtools import get_femnodes_by_refshape as getnodes
        getnodes(femmesh, ref)

    def tearDown(self):
        # clearance, is executed after every test
        FreeCAD.closeDocument(self.doc_name)
        pass


'''

# to do, prints in meshtools


make -j4 && ./bin/FreeCADCmd --run-test "femtest.app.test_cmdproblem.TestCmdProblem.test_face_subclass1"
make -j4 && ./bin/FreeCADCmd --run-test "femtest.app.test_cmdproblem.TestCmdProblem.test_face_subclass2"
make -j4 && ./bin/FreeCADCmd --run-test "femtest.app.test_cmdproblem.TestCmdProblem.test_cmdproblem"

import unittest

unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromName("femtest.app.test_cmdproblem.TestCmdProblem.test_cmdproblem"))

unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromName("femtest.app.test_cmdproblem.TestCmdProblem.test_face_subclass1"))
unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromName("femtest.app.test_cmdproblem.TestCmdProblem.test_face_subclass2"))



# ************************************************************************************************
# https://forum.freecadweb.org/viewtopic.php?f=10&t=36543

# the origin test, which does not work for me on my dev machine is:

make -j4 && ./bin/FreeCADCmd --run-test "femtest.app.test_ccxtools.TestCcxTools.test_1_static_analysis"

import unittest
unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromName("femtest.app.test_ccxtools.TestCcxTools.test_1_static_analysis"))



Writing /tmp/FEM_unittests/FEM_ccx_static/Mesh.inp for static analysis 
Start writing CalculiX input file
writerbaseCcx --> self.file_name  -->  /tmp/FEM_unittests/FEM_ccx_static/Mesh.inp
Constraint fixed: FemConstraintFixed
  Finite element mesh nodes will be retrieved by searching the appropriate nodes in the finite element mesh.
(<Part::PartFeature>, ('Face1',))
  ReferenceShape ... Type: Face, Object name: Box, Object label: Box, Element name: Face1
<Face object at 0x55b0c0b5e970>
<class 'Part.Face'>
Face
False
<class 'Part.Face'>
True
Unexpected error when writing CalculiX input file: <class 'TypeError'>
ERROR

======================================================================
ERROR: test_1_static_analysis (femtest.app.test_ccxtools.TestCcxTools)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femtest/app/test_ccxtools.py", line 231, in test_1_static_analysis
    error = fea.write_inp_file()
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femtools/ccxtools.py", line 755, in write_inp_file
    self.inp_file_name = inp_writer.write_calculix_input_file()
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femsolver/calculix/writer.py", line 114, in write_calculix_input_file
    self.write_calculix_one_input_file()
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femsolver/calculix/writer.py", line 144, in write_calculix_one_input_file
    self.write_node_sets_constraints_fixed(inpfile)
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femsolver/calculix/writer.py", line 502, in write_node_sets_constraints_fixed
    self.get_constraints_fixed_nodes()
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femsolver/writerbase.py", line 133, in get_constraints_fixed_nodes
    femobj
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femmesh/meshtools.py", line 52, in get_femnodes_by_femobj_with_references
    node_set = get_femnodes_by_references(femmesh, femobj["Object"].References)
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femmesh/meshtools.py", line 98, in get_femnodes_by_references
    references_femnodes += get_femnodes_by_refshape(femmesh, ref)
  File "/home/hugo/Documents/dev/freecad/freecadbhb_dev/build/Mod/Fem/femmesh/meshtools.py", line 135, in get_femnodes_by_refshape
    nodes += femmesh.getNodesByFace(r)
TypeError: argument 1 must be Part.TopoShape, not Part.Face

----------------------------------------------------------------------
Ran 1 test in 0.084s

FAILED (errors=1)

'''
