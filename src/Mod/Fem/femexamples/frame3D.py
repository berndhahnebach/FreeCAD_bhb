# ***************************************************************************
# *   Copyright (c) 2020 Raeyat Roknabadi Ebrahim <ebe79442114@yahoo.com>   *
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


# to run the example use:
"""
from femexamples import frame3D
frame3D.setup()

"""

import FreeCAD
from FreeCAD import Vector as vec

import BOPTools.SplitFeatures
import Draft

import Fem
import ObjectsFem

mesh_name = "Mesh"  # needs to be Mesh to work with unit tests


def init_doc(doc=None):
    if doc is None:
        doc = FreeCAD.newDocument()
    return doc


def setup(doc=None, solvertype="opensees"):
    # setup model

    if doc is None:
        doc = init_doc()

    # geometry object
    p1 = vec(0.000, 1890.000, 5300.000)
    p2 = vec(0.000, 5130.000, 5300.000)
    p3 = vec(0.000, 9410.000, 5300.000)
    p4 = vec(4210.000, 5130.000, 5300.000)
    p5 = vec(6450.000, 9410.000, 5300.000)
    p6 = vec(0.000, 0.000, 5300.000)
    p7 = vec(5725.000, 4200.000, 5300.000)
    p8 = vec(7948.416, 9410.000, 5300.000)
    p9 = vec(0.000, 9410.000, -200.000)
    p10 = vec(6450.000, 9410.000, -200.000)
    p11 = vec(4210.000, 5130.000, -200.000)
    p12 = vec(0.000, 5130.000, -200.000)
    p13 = vec(0.000, 1890.000, -200.000)

    l1 = Draft.makeLine(p1, p2)
    l2 = Draft.makeLine(p2, p3)
    l3 = Draft.makeLine(p1, p4)
    l4 = Draft.makeLine(p4, p5)
    l5 = Draft.makeLine(p3, p5)
    l6 = Draft.makeLine(p2, p4)
    l7 = Draft.makeLine(p6, p1)
    l8 = Draft.makeLine(p4, p7)
    l9 = Draft.makeLine(p5, p8)
    l10 = Draft.makeLine(p9, p3)
    l11 = Draft.makeLine(p10, p5)
    l12 = Draft.makeLine(p11, p4)
    l13 = Draft.makeLine(p12, p2)
    l14 = Draft.makeLine(p13, p1)

    lines = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14]

    geom_obj = BOPTools.SplitFeatures.makeBooleanFragments(name='BooleanFragments')
    geom_obj.Objects = lines
    # j.Mode = 'Standard'
    # j.Proxy.execute(j)
    # j.purgeTouched()
    for obj in geom_obj.ViewObject.Proxy.claimChildren():
        obj.ViewObject.hide()

    doc.recompute()

    if FreeCAD.GuiUp:
        geom_obj.ViewObject.Document.activeView().viewAxonometric()
        geom_obj.ViewObject.Document.activeView().fitAll()

    # analysis and solver
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")
    analysis.addObject(ObjectsFem.makeSolverOpenSees(doc, "SolverOpenSees"))

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

    # force_constraint
    force_constraint = analysis.addObject(
        ObjectsFem.makeConstraintForce(doc, name="ConstraintForce")
    )[0]
    force_constraint.References = [(geom_obj, "Vertex4")]
    force_constraint.Force = 5.0
    # force_constraint.Direction = (doc.Face, ["Edge2"])
    # force_constraint.Reversed = False

    # fixed_constraint
    fixed_constraint = analysis.addObject(
        ObjectsFem.makeConstraintFixed(doc, name="ConstraintFixed")
    )[0]
    fixed_constraint.References = [(geom_obj, f"Vertex{i}") for i in range(9, 14)]

    # beamsections
    beams = analysis.addObject(
        ObjectsFem.makeElementGeometry1D(doc, name="ElementGeometry1D"))[0]
    beams.Label = "Beams"
    beams.References = [(geom_obj, f"Edge{i}") for i in range(1, 10)]
    beams.SectionType = "Rectangular"
    beams.RectHeight = "500 mm"
    beams.RectWidth = "400 mm"

    cols = analysis.addObject(
        ObjectsFem.makeElementGeometry1D(doc, name="ElementGeometry1D"))[0]
    cols.Label = "Columns"
    cols.References = [(geom_obj, f"Edge{i}") for i in range(10, 15)]
    cols.SectionType = "Rectangular"
    cols.RectHeight = "600 mm"
    cols.RectWidth = "600 mm"

    # mesh
    from .meshes.mesh_frame3D_seg3 import create_nodes, create_elements
    fem_mesh = Fem.FemMesh()
    control = create_nodes(fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating nodes.\n")
    control = create_elements(fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating elements.\n")
    femmesh_obj = analysis.addObject(
        ObjectsFem.makeMeshGmsh(doc, name="Mesh")
    )[0]
    femmesh_obj.FemMesh = fem_mesh
    femmesh_obj.Part = geom_obj

    doc.recompute()
    return doc
