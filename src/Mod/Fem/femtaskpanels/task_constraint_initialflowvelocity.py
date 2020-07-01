# ***************************************************************************
# *   Copyright (c) 2017 Markus Hovorka <m.hovorka@live.de>                 *
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
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

__title__ = "FreeCAD FEM constraint initial flow velocity task panel for the document object"
__author__ = "Markus Hovorka, Bernd Hahnebach"
__url__ = "https://www.freecadweb.org"

## @package task_constraint_initialflowvelocity
#  \ingroup FEM
#  \brief task panel for constraint initial flow velocity object

import FreeCAD
import FreeCADGui
from FreeCAD import Units

from femtools import femutils
from femtools import membertools


class _TaskPanel(object):

    def __init__(self, obj):
        self._obj = obj
        self._paramWidget = FreeCADGui.PySideUic.loadUi(
            FreeCAD.getHomePath() + "Mod/Fem/Resources/ui/InitialFlowVelocity.ui")
        self._initParamWidget()
        self.form = [self._paramWidget]
        analysis = obj.getParentGroup()
        self._mesh = None
        self._part = None
        if analysis is not None:
            self._mesh = membertools.get_single_member(analysis, "Fem::FemMeshObject")
        if self._mesh is not None:
            self._part = femutils.get_part_to_mesh(self._mesh)
        self._partVisible = None
        self._meshVisible = None

    def open(self):
        if self._mesh is not None and self._part is not None:
            self._meshVisible = self._mesh.ViewObject.isVisible()
            self._partVisible = self._part.ViewObject.isVisible()
            self._mesh.ViewObject.hide()
            self._part.ViewObject.show()

    def reject(self):
        FreeCADGui.ActiveDocument.resetEdit()
        self._restoreVisibility()
        return True

    def accept(self):
        self._applyWidgetChanges()
        self._obj.Document.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        self._restoreVisibility()
        return True

    def _restoreVisibility(self):
        if self._mesh is not None and self._part is not None:
            if self._meshVisible:
                self._mesh.ViewObject.show()
            else:
                self._mesh.ViewObject.hide()
            if self._partVisible:
                self._part.ViewObject.show()
            else:
                self._part.ViewObject.hide()

    def _initParamWidget(self):
        unit = "m/s"
        self._paramWidget.velocityXTxt.setText(
            str(self._obj.VelocityX) + unit)
        self._paramWidget.velocityYTxt.setText(
            str(self._obj.VelocityY) + unit)
        self._paramWidget.velocityZTxt.setText(
            str(self._obj.VelocityZ) + unit)
        self._paramWidget.velocityXBox.setChecked(
            not self._obj.VelocityXEnabled)
        self._paramWidget.velocityYBox.setChecked(
            not self._obj.VelocityYEnabled)
        self._paramWidget.velocityZBox.setChecked(
            not self._obj.VelocityZEnabled)

    def _applyWidgetChanges(self):
        unit = "m/s"
        self._obj.VelocityXEnabled = \
            not self._paramWidget.velocityXBox.isChecked()
        if self._obj.VelocityXEnabled:
            quantity = None
            userinput = (self._paramWidget.velocityXTxt.text())
            try:
                quantity = Units.Quantity(self._paramWidget.velocityXTxt.text())
            except:
                print(userinput)
            if quantity is not None and Units.Unit(quantity) == Units.Velocity:
                # exception if no Unit is given ???
                self._obj.VelocityX = float(quantity.getValueAs(unit))
            else:
                # see on file end
                # user might have input a number without unit, m/s
                # float(self._paramWidget.velocityXTxt.text())
                print("Wrong input.")
                print(userinput)
                # handle no unit with elif, because it is valid input, but print information
        self._obj.VelocityYEnabled = \
            not self._paramWidget.velocityYBox.isChecked()
        if self._obj.VelocityYEnabled:
            quantity = Units.Quantity(self._paramWidget.velocityYTxt.text())
            self._obj.VelocityY = float(quantity.getValueAs(unit))
        self._obj.VelocityZEnabled = \
            not self._paramWidget.velocityZBox.isChecked()
        if self._obj.VelocityZEnabled:
            quantity = Units.Quantity(self._paramWidget.velocityZTxt.text())
            self._obj.VelocityZ = float(quantity.getValueAs(unit))


"""
# may be use rawProperty, see old material panel
# if tackled down use on any input field in Python (femguiutils)
# here and material task panel
# forum link:
# https://forum.freecadweb.org/viewtopic.php?t=46873
# https://forum.freecadweb.org/viewtopic.php?&t=24015
# local on my machine: ein input widget pop up to test
# /home/hugo/Documents/projekte--freecad/prj_verschiedene/qtreeatributes/widget_test/
# mein unts file on desktop
# add from unts file to cardutils or all the the new method on femguiutils


from FreeCAD import Units
getattr(Units, 'Pressure')
Units.Pressure
Units.Quantity('25 MPa')
Units.Quantity('25 MPa').getValueAs('Pa')
Units.Quantity('25 MPa').getUserPreferred()[2]
Units.Quantity(25000, Units.Pressure)
Units.Quantity(25000, Units.Pressure).getValueAs('MPa')
Units.Unit('25 MPa')
Units.Unit(-1,1,-2,0,0,0,0,0)


Units.Unit('MPa')
Units.Unit('kg/(mm*s^2)')
Units.Unit('t/(m*min^2)')
Units.Pressure


Units.Unit('MPa') == Units.Pressure
Units.Unit('MPa') == Units.Length
Units.Unit('mm') == Units.Pressure
Units.Unit('mm') == Units.Length
Units.Unit('t/(m*min^2)') == Units.Unit('MPa')


Units.Quantity('5')


# in cmd FreeCAD is exited
from FreeCAD import Units
myquantity = Units.Quantity('500')
Units.Unit(myquantity)

from FreeCAD import Units
myquantity = Units.Quantity('5')
Units.Unit(myquantity)


# exception, Unit mismatch
Units.Quantity('25 ').getValueAs('Pa')


# add to cardutils examples, or all in femguiutils


Units.Unit(Units.Quantity('5 MPa'))
Units.Unit(Units.Quantity('5 Mpa'))
Units.Unit(Units.Quantity('MPa'))
Units.Unit(Units.Quantity('Mpa'))

Units.Quantity('5')


from FreeCAD import Units
Units.Unit(Units.Quantity('500'))
Units.Unit(Units.Quantity('5'))
Units.Unit(Units.Quantity('-5'))



# some unit code **********
from FreeCAD import Units
getattr(Units, 'Pressure')
Units.Pressure
Units.Quantity('25 MPa')
Units.Quantity('25 MPa').getValueAs('Pa')
Units.Quantity('25 MPa').getUserPreferred()[2]
Units.Quantity(25000, Units.Pressure)
Units.Quantity(25000, Units.Pressure).getValueAs('MPa')
Units.Pressure
Units.Unit('25 MPa')
Units.Unit(-1,1,-2,0,0,0,0,0)

# base units
from FreeCAD import Units
Units.Length
Units.Mass
Units.TimeSpan
Units.ElectricCurrent
Units.Temperature
Units.AmountOfSubstance
Units.LuminousIntensity
Units.Angle



Units.Quantity('50 MPa')
type(Units.Quantity('50 MPa'))

>>>
>>> Units.Quantity('50 MPa')
50000.0 kg/(mm*s^2)
>>> type(Units.Quantity('50 MPa'))
<class 'Base.Quantity'>
>>>


Units.Pressure
Units.Unit('25 MPa')
Units.Unit(-1,1,-2,0,0,0,0,0)
type(Units.Pressure)

>>>
>>> Units.Pressure
Unit: kg/(mm*s^2) (-1,1,-2,0,0,0,0,0) [Pressure]
>>> Units.Unit('25 MPa')
Unit: kg/(mm*s^2) (-1,1,-2,0,0,0,0,0) [Pressure]
>>> Units.Unit(-1,1,-2,0,0,0,0,0)
Unit: kg/(mm*s^2) (-1,1,-2,0,0,0,0,0) [Pressure]
>>> type(Units.Pressure)
<class 'Base.Unit'>
>>>


from FreeCAD import Units

q1 = Units.Quantity('500 MPa')
q1.Unit
Units.Unit(q1)

q2 = Units.Quantity('500')
q2.Unit
Units.Unit(q2)

q3 = Units.Quantity('5')
q3.Unit
Units.Unit(q3)


# src/Base/UnitPy.xml

Unit
defines a unit type, calculate and compare.

The following constructors are supported:
Unit()                        -- empty constructor
Unit(i1,i2,i3,i4,i5,i6,i7,i8) -- unit signature
Unit(Quantity)                -- copy unit from Quantity
Unit(Unit)                    -- copy constructor
Unit(string)                  -- parse the string for units

Quantity
defined by a value and a unit.

The following constructors are supported:
Quantity() -- empty constructor
Quantity(Value) -- empty constructor
Quantity(Value,Unit) -- empty constructor
Quantity(Quantity) -- copy constructor
Quantity(string) -- arbitrary mixture of numbers and chars defining a Quantity


"""
