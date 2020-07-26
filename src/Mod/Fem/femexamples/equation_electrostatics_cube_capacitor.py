# ***************************************************************************
# *   Copyright (c) 2020 Sudhanshu Dubey <sudhanshu.thethunder@gmail.com>   *
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

# to run the example use:
"""
from femexamples.equation_electrostatics_cube_capacitor import setup
setup()
"""
# Electrostatics Cube Capacitor
# https://forum.freecadweb.org/viewtopic.php?f=18&t=41488&start=60#p401652

import FreeCAD

import Fem
import ObjectsFem

mesh_name = "Mesh"  # needs to be Mesh to work with unit tests


def init_doc(doc=None):
    if doc is None:
        doc = FreeCAD.newDocument()
    return doc


def get_information():
    info = {"name": "Electrostatics Cube Capacitor",
            "meshtype": "solid",
            "meshelement": "Tet10",
            "constraints": ["electrostatic potential"],
            "solvers": ["elmer"],
            "material": "fluid",
            "equation": "electrostatic"
            }
    return info


def setup(doc=None, solvertype="elmer"):
    # setup base model

    if doc is None:
        doc = init_doc()

    # geometry object
    # name is important because the other method in this module use obj name
    geom_obj = doc.addObject("Part::Box", "Box")
    geom_obj.Height = geom_obj.Width = geom_obj.Length = 1000
    doc.recompute()

    if FreeCAD.GuiUp:
        geom_obj.ViewObject.Document.activeView().viewAxonometric()
        geom_obj.ViewObject.Document.activeView().fitAll()

    # analysis
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    # solver
    if solvertype == "elmer":
        solver_object = analysis.addObject(ObjectsFem.makeSolverElmer(doc, "SolverElmer"))[0]
        eq_electrostatic = ObjectsFem.makeEquationElectrostatic(doc, solver_object)
        eq_electrostatic.CalculateCapacitanceMatrix = True
    else:
        FreeCAD.Console.PrintWarning(
            "Not known or not supported solver type: {}. "
            "No solver object was created.\n".format(solvertype)
        )

    # material
    material_object = analysis.addObject(
        ObjectsFem.makeMaterialFluid(doc, "FemMaterial")
    )[0]
    mat = material_object.Material
    mat["Name"] = "Air-Generic"
    mat["Density"] = "1.20 kg/m^3"
    mat["KinematicViscosity"] = "15.11 mm^2/s"
    mat["VolumetricThermalExpansionCoefficient"] = "0.00 µm/m/K"
    mat["ThermalConductivity"] = "0.03 W/m/K"
    mat["ThermalExpansionCoefficient"] = "0.0034/K"
    mat["SpecificHeat"] = "1.00 J/kg/K"
    mat["RelativePermittivity"] = "1.00"
    material_object.Material = mat

    # 1st potential_constraint
    constraint_elect_pot0 = analysis.addObject(
        ObjectsFem.makeConstraintElectrostaticPotential(doc))[0]
    constraint_elect_pot0.References = [(geom_obj, "Face6")]
    constraint_elect_pot0.PotentialEnabled = True
    constraint_elect_pot0.Potential = 2.00
    constraint_elect_pot0.CapacitanceBodyEnabled = True
    constraint_elect_pot0.CapacitanceBody = 1

    # 2nd potential_constraint
    constraint_elect_pot1 = analysis.addObject(
        ObjectsFem.makeConstraintElectrostaticPotential(doc))[0]
    constraint_elect_pot1.References = [(geom_obj, "Face5")]
    constraint_elect_pot1.PotentialEnabled = True
    constraint_elect_pot1.Potential = -1.00
    constraint_elect_pot1.CapacitanceBodyEnabled = True
    constraint_elect_pot1.CapacitanceBody = 2

    # mesh
    from .meshes.mesh_cube_capacitor_tetra10 import create_nodes, create_elements
    fem_mesh = Fem.FemMesh()
    control = create_nodes(fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating nodes.\n")
    control = create_elements(fem_mesh)
    if not control:
        FreeCAD.Console.PrintError("Error on creating elements.\n")
    femmesh_obj = analysis.addObject(
        ObjectsFem.makeMeshGmsh(doc, mesh_name)
    )[0]
    femmesh_obj.FemMesh = fem_mesh
    femmesh_obj.Part = geom_obj
    femmesh_obj.SecondOrderLinear = False

    doc.recompute()
    return doc
