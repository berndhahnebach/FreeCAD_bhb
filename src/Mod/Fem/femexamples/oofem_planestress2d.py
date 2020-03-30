# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
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
# ***************************************************************************

# setup oofem manual example PlaneStress2D.in
# http://www.oofem.org/resources/doc/oofemInput/html/oofemInput.html
# http://www.oofem.org/resources/doc/oofemInput/html/node61.html

# to run the example use:
"""
from femexamples.oofem_planestress2d import setup
setup()

"""

import FreeCAD

import Fem
import ObjectsFem

mesh_name = "Mesh"  # needs to be Mesh to work with unit tests


def init_doc(doc=None):
    if doc is None:
        doc = FreeCAD.newDocument()
    return doc


def get_information():
    info = {
        "name": "2D plane stress",
        "meshtype": "shell",
        "meshelement": "Quad4",
        "constraints": ["displacement", "force"],
        "solvers": ["oofem"],
        "material": "solid",
        "equation": "mechanical"
    }
    return info


def setup(doc=None, solvertype="oofem"):
    # setup model

    if doc is None:
        doc = init_doc()

    # geometry object
    geom_obj = doc.addObject("Part::Plane", "Face")
    geom_obj.Width = 4
    geom_obj.Length = 9
    doc.recompute()

    if FreeCAD.GuiUp:
        geom_obj.ViewObject.Document.activeView().viewAxonometric()
        geom_obj.ViewObject.Document.activeView().fitAll()

    # analysis and solver
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")
    analysis.addObject(ObjectsFem.makeSolverOofem(doc, "SolverOOFEM"))

    # shell thickness
    thickness_obj = analysis.addObject(
        ObjectsFem.makeElementGeometry2D(doc, 0, "ShellThickness")
    )[0]
    thickness_obj.Thickness = 1.0

    # materials
    material_object = analysis.addObject(
        ObjectsFem.makeMaterialSolid(doc, "FemMaterial")
    )[0]
    mat = {}
    mat["Name"] = "Concrete-Generic"
    mat["YoungsModulus"] = "15 MPa"
    mat["PoissonRatio"] = "0.25"
    mat["Density"] = "0.0 kg/m^3"
    mat["ThermalExpansionCoefficient"] = "1.0 m/m/K"
    material_object.Material = mat

    # displacement_constraints
    # festes lager
    displacement_constraint1 = analysis.addObject(
        ObjectsFem.makeConstraintDisplacement(doc, name="ConstraintDisplacmentFest")
    )[0]
    displacement_constraint1.References = [(geom_obj, "Vertex1"), (geom_obj, "Vertex2")]
    displacement_constraint1.xFix = True
    displacement_constraint1.xFree = False
    displacement_constraint1.xDisplacement = 0.0
    displacement_constraint1.yFix = True
    displacement_constraint1.yFree = False
    displacement_constraint1.yDisplacement = 0.0
    # hozizontal bewegliches lager (Gleitlager)
    displacement_constraint2 = analysis.addObject(
        ObjectsFem.makeConstraintDisplacement(doc, name="ConstraintDisplacmentGleit")
    )[0]
    displacement_constraint2.References = [(geom_obj, "Vertex3"), (geom_obj, "Vertex4")]
    displacement_constraint2.yFix = True
    displacement_constraint2.yFree = False
    displacement_constraint2.xDisplacement = 0.0

    # force_constraint
    force_constraint = analysis.addObject(
        ObjectsFem.makeConstraintForce(doc, name="ConstraintForce")
    )[0]
    force_constraint.References = [(geom_obj, "Vertex3"), (geom_obj, "Vertex4")]
    force_constraint.Force = 5.0  # two nodes each 2.5 N = 5.0 N
    force_constraint.Direction = (doc.Face, ["Edge2"])
    force_constraint.Reversed = False

    # mesh
    fem_mesh = Fem.FemMesh()
    fem_mesh.addNode(0.0, 0.0, 0.0, 1)
    fem_mesh.addNode(0.0, 4.0, 0.0, 2)
    fem_mesh.addNode(2.0, 2.0, 0.0, 3)
    fem_mesh.addNode(3.0, 1.0, 0.0, 4)
    fem_mesh.addNode(8.0, 0.8, 0.0, 5)
    fem_mesh.addNode(7.0, 3.0, 0.0, 6)
    fem_mesh.addNode(9.0, 0.0, 0.0, 7)
    fem_mesh.addNode(9.0, 4.0, 0.0, 8)
    fem_mesh.addFace([1, 4, 3, 2], 1)
    fem_mesh.addFace([1, 7, 5, 4], 2)
    fem_mesh.addFace([4, 5, 6, 3], 3)
    fem_mesh.addFace([3, 6, 8, 2], 4)
    fem_mesh.addFace([5, 7, 8, 6], 5)
    femmesh_obj = analysis.addObject(doc.addObject("Fem::FemMeshObject", mesh_name))[0]
    femmesh_obj.FemMesh = fem_mesh

    doc.recompute()
    return doc
