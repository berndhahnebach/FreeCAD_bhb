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
from femexamples.curved_pipe_heat_flow import setup
setup()

"""

# Heat flow in a curved pipe
# https://forum.freecadweb.org/viewtopic.php?f=18&t=22576&start=130#p194708

import FreeCAD
from FreeCAD import Vector
from FreeCAD import Units

import Fem
import ObjectsFem
import Part
import Sketcher
from BOPTools.SplitFeatures import makeBooleanFragments

mesh_name = "Mesh"  # needs to be Mesh to work with unit tests


def init_doc(doc=None):
    if doc is None:
        doc = FreeCAD.newDocument()
    return doc


def get_information():
    info = {"name": "Cuved Pipe Heat Flow",
            "meshtype": "solid",
            "meshelement": "Tet10",
            "constraints": ["temperature", "flow velocity"],
            "solvers": ["elmer"],
            "material": "multimaterial",
            "equation": "heat"
            }
    return info


def setup(doc=None, solvertype="elmer"):

    if doc is None:
        doc = init_doc()

    # outer_pipe
    outer = doc.addObject('PartDesign::Body', 'Outer')

    outer_circle = outer.newObject('Sketcher::SketchObject', 'Outer_Circle')
    outer_circle.Support = (doc.getObject('YZ_Plane'), [''])
    outer_circle.MapMode = 'FlatFace'
    outer_circle.addGeometry(
        Part.Circle(Vector(0.0, 0.0, 0), Vector(0, 0, 1), 12.0),
        False
    )
    outer_circle.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
    outer_circle.addConstraint(Sketcher.Constraint('Radius', 0, 12.000000))
    outer_circle.setDatum(1, Units.Quantity('12.0 mm'))

    outer_spine = outer.newObject('Sketcher::SketchObject', 'Outer_Spine')
    outer_spine.Support = (doc.getObject('XZ_Plane'), [''])
    outer_spine.MapMode = 'FlatFace'
    spine_geolist = [
        Part.LineSegment(Vector(0.0, -0.0, 0), Vector(-25.706558, 0.114256, 0)),
        Part.ArcOfCircle(
            Part.Circle(Vector(-30.505114, 15.877316, 0), Vector(0, 0, 1), 20.0),
            -3.847513,
            -1.538994),
        Part.LineSegment(Vector(-49.405247, 26.265810, 0), Vector(-23.650030, 40.555614, 0))
    ]
    outer_spine.addGeometry(spine_geolist, False)
    spine_conlist = [
        Sketcher.Constraint('Horizontal', 0),
        Sketcher.Constraint('Coincident', 1, 2, 0, 2),
        Sketcher.Constraint('Coincident', 1, 1, 2, 1),
        Sketcher.Constraint('Coincident', 0, 1, -1, 1),
        Sketcher.Constraint('Tangent', 0, 1),
        Sketcher.Constraint('Tangent', 2, 1),
        Sketcher.Constraint('Equal', 2, 0),
        Sketcher.Constraint('DistanceX', 0, 2, 0, 1, 29.806131),
        Sketcher.Constraint('Radius', 1, 14.600795),
        Sketcher.Constraint('Angle', 0, 2, 2, 1, 0.336732)
    ]
    outer_spine.addConstraint(spine_conlist)
    outer_spine.setDatum(7, Units.Quantity('30.0 mm'))
    outer_spine.setDatum(8, Units.Quantity('20.0 mm'))
    outer_spine.setDatum(9, Units.Quantity('45.0 deg'))

    outer_pipe = outer.newObject('PartDesign::AdditivePipe', 'Outer_Pipe')
    outer_pipe.Profile = outer_circle
    outer_pipe.Spine = outer_spine

    # inner pipe
    inner = doc.addObject('PartDesign::Body', 'Inner')

    inner_circle = inner.newObject('Sketcher::SketchObject', 'Inner_Circle')
    inner_circle.Support = (doc.getObject('YZ_Plane'), [''])
    inner_circle.MapMode = 'FlatFace'
    inner_circle.addGeometry(
        Part.Circle(Vector(0.0, 0.0, 0), Vector(0, 0, 1), 12.0),
        False
    )
    inner_circle.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
    inner_circle.addConstraint(Sketcher.Constraint('Radius', 0, 10.000000))
    inner_circle.setDatum(1, Units.Quantity('10.0 mm'))

    inner_spine = inner.newObject('Sketcher::SketchObject', 'Inner_Spine')
    inner_spine.Support = (doc.getObject('XZ_Plane'), [''])
    inner_spine.MapMode = 'FlatFace'
    inner_spine.addGeometry(spine_geolist, False)
    inner_spine.addConstraint(spine_conlist)
    inner_spine.setDatum(7, Units.Quantity('30.0 mm'))
    inner_spine.setDatum(8, Units.Quantity('20.0 mm'))
    inner_spine.setDatum(9, Units.Quantity('45.0 deg'))

    inner_pipe = inner.newObject('PartDesign::AdditivePipe', 'Inner_Pipe')
    inner_pipe.Profile = inner_circle
    inner_pipe.Spine = inner_spine

    # geometry object
    geom_obj = makeBooleanFragments(name='BooleanFragments')
    geom_obj.Objects = [outer, inner]
    geom_obj.Mode = 'Standard'
    geom_obj.purgeTouched()
    if FreeCAD.GuiUp:
        outer.ViewObject.hide()
        inner.ViewObject.hide()
    doc.recompute()

    if FreeCAD.GuiUp:
        geom_obj.ViewObject.Transparency = 50
        geom_obj.ViewObject.Document.activeView().viewAxonometric()
        geom_obj.ViewObject.Document.activeView().fitAll()

    # analysis
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    # solver
    if solvertype == "elmer":
        solver_object = analysis.addObject(ObjectsFem.makeSolverElmer(doc, "SolverElmer"))[0]
        eq_heat = ObjectsFem.makeEquationHeat(doc, solver_object)
        eq_heat.References = [(geom_obj, "Solid1"), (geom_obj, "Solid2")]
        eq_heat.LinearPreconditioning = "ILU1"
        eq_heat.LinearTolerance = 0.0001
        eq_heat.Priority = 20
        eq_heat.SteadyStateTolerance = 0.0001
        eq_flow = ObjectsFem.makeEquationFlow(doc, solver_object)
        eq_flow.References = [(geom_obj, "Solid2")]
        eq_flow.LinearPreconditioning = "ILU1"
        eq_flow.LinearTolerance = 0.0001
        eq_flow.Priority = 30
        eq_flow.SteadyStateTolerance = 0.0001
    else:
        FreeCAD.Console.PrintWarning(
            "Not known or not supported solver type: {}. "
            "No solver object was created.\n".format(solvertype)
        )

    # solid_material
    material_object1 = analysis.addObject(
        ObjectsFem.makeMaterialSolid(doc, "SolidMaterial")
    )[0]
    material_object1.References = [(geom_obj, "Solid1")]
    mat = material_object1.Material
    mat["Name"] = "Steel-Generic"
    mat["YoungsModulus"] = "200000 MPa"
    mat["PoissonRatio"] = "0.30"
    mat["SpecificHeat"] = "500.0 J/kg/K"
    mat["ThermalConductivity"] = "50.0 W/m/K"
    mat["ThermalExpansionCoefficient"] = "12.0 um/m/K"
    mat["Density"] = "7900.0 kg/m^3"
    material_object1.Material = mat

    # fluid_material
    material_object2 = analysis.addObject(
        ObjectsFem.makeMaterialFluid(doc, "FluidMaterial")
    )[0]
    material_object2.References = [(geom_obj, "Solid2")]
    mat = material_object2.Material
    mat["Name"] = "Water"
    mat["DynamicViscosity"] = "1.003e-3 kg/m/s"
    mat["KinematicViscosity"] = "1.004e-6 m^2/s"
    mat["SpecificHeat"] = "4183 J/kg/K"
    mat["ThermalConductivity"] = "0.591 W/m/K"
    mat["ThermalExpansionCoefficient"] = "0 um/m/K"
    mat["Density"] = "998.0 kg/m^3"
    mat["MolarMass"] = "18"
    mat["VolumetricThermalExpansionCoefficient"] = "0 m^3/m^3/K"
    material_object2.Material = mat

    # temperature_constraint
    temperature_constraint = analysis.addObject(
        ObjectsFem.makeConstraintTemperature(doc, "Inlet_Temperature")
    )[0]
    temperature_constraint.References = [(geom_obj, "Face10")]
    temperature_constraint.Temperature = 350.00

    # velocity_constraint1
    inlet_vel_constraint = analysis.addObject(
        ObjectsFem.makeConstraintFlowVelocity(doc, "Inlet_Velocity")
    )[0]
    inlet_vel_constraint.References = [(geom_obj, "Face10")]
    inlet_vel_constraint.VelocityXEnabled = True
    inlet_vel_constraint.VelocityYEnabled = True
    inlet_vel_constraint.VelocityZEnabled = True
    inlet_vel_constraint.VelocityZ = 0.01

    # velocity_constraint2
    noslip_vel_constraint = analysis.addObject(
        ObjectsFem.makeConstraintFlowVelocity(doc, "NoSlip_Velocity")
    )[0]
    noslip_vel_constraint.References = [
        (geom_obj, "Face3"),
        (geom_obj, "Face5"),
        (geom_obj, "Face7")]
    noslip_vel_constraint.VelocityXEnabled = True
    noslip_vel_constraint.VelocityYEnabled = True
    noslip_vel_constraint.VelocityZEnabled = True

    return doc
