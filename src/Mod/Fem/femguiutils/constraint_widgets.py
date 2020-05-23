# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2018 qingfeng Xia <qingfeng.xia@gmail.coom>             *
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

__title__ = "body source and initial value setup"
__author__ = "Qingfeng Xia"
__url__ = "http://www.freecadweb.org"

## @package FemBodyConstraint
#  \ingroup FEM
#  \brief QWidget for FEM general body source and initial value setup

import sys

# import FreeCAD
# from FreeCAD import Units
# import FreeCADGui as Gui

# from PySide import QtCore
# preparing for PySide2 Qt5
from PySide.QtGui import QApplication
from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, \
    QButtonGroup, QRadioButton, QLineEdit, QDoubleSpinBox, QLabel


def _createChoiceGroup(valueTypes, valueTypeTips):
        _buttonGroupLayout = QHBoxLayout()
        buttonGroupValueType = QButtonGroup()
        buttonGroupValueType.setExclusive(True)

        for id, choice in enumerate(valueTypes):
            rb = QRadioButton(choice)
            rb.setToolTip(valueTypeTips[id])
            buttonGroupValueType.addButton(rb, id)
            _buttonGroupLayout.addWidget(rb)
            if id == 0:
                rb.setChecked(True)
        return buttonGroupValueType, _buttonGroupLayout


class ConstraintInputWidget(QWidget):
    # QWidget that can be included into FreeCAD taskpanel or used as standalone UI
    def __init__(self, constraintSettings):
        super(ConstraintInputWidget, self).__init__()

        bcs = constraintSettings  # must existing
        self.settings = bcs
        if bcs["Category"] == "InitialValue":
            self.setWindowTitle(self.tr("set initial value"))
        elif bcs["Category"] == "Source":
            self.setWindowTitle(self.tr("set body source"))
        else:
            self.setWindowTitle(self.tr("set constraint input"))

        self.numberOfComponents = bcs["NumberOfComponents"]
        unit = bcs["Unit"]

        _layout = QVBoxLayout()
        self.labelHelpText = QLabel(
            self.tr("set physical quantity by float or expression"),
        )

        self.valueTypes = ["Quantity", "Expression"]
        valueTypeTips = [
            self.tr("float value for each component"),
            self.tr("math expressiong using xyz coord")
        ]
        self.buttonGroupValueType, _buttonGroupLayout = _createChoiceGroup(
            self.valueTypes, valueTypeTips
        )
        # diff connect syntax
        self.buttonGroupValueType.buttonClicked.connect(self.valueTypeChanged)

        _gridLayout = QGridLayout()
        if self.numberOfComponents == 1:
            self.componentLabels = ["magnitude"]
        else:
            self.componentLabels = ["x-component", "y-component", "z-component"]
        self.componentLabels = [l + " ({})".format((unit)) for l in self.componentLabels]
        self.quantityInputs = []
        self.expressionInputs = []
        for i in range(self.numberOfComponents):
            input = QDoubleSpinBox()  # Gui.InputField() depends on FreeCAD
            input.setRange(-1e10, 1e10)  # give a range big enough
            input.setValue(0.0)
            expr = QLineEdit()  # QTextEdit is too big
            _gridLayout.addWidget(QLabel(self.componentLabels[i]), i, 0)
            _gridLayout.addWidget(input, i, 1)
            _gridLayout.addWidget(expr, i, 2)
            self.quantityInputs.append(input)
            self.expressionInputs.append(expr)

        _layout.addWidget(self.labelHelpText)
        _layout.addLayout(_buttonGroupLayout)
        _layout.addLayout(_gridLayout)
        self.setLayout(_layout)

        self.updateUI(self.settings)

    def updateUI(self, settings):
        # fill setting data into UI, possibibly value is empty
        vtype = settings["ValueType"]
        try:
            index = self.valueTypes.index(vtype)
        except ValueError:
            index = 0
        for button in self.buttonGroupValueType.buttons():
            if self.buttonGroupValueType.id(button) == index:
                button.setChecked(True)
        self.valueTypeChanged()

        value = settings["Value"] if ("Value" in settings) else None
        if value is None:
            return
        if not isinstance(value, (list, tuple)) and settings["NumberOfComponents"] == 1:
            value = [value]
        for i in range(self.numberOfComponents):
            if settings["ValueType"] == "Expression":
                self.expressionInputs[i].setText(str(value[i]))
            else:
                self.quantityInputs[i].setValue(value[i])

    def valueTypeChanged(self):
        # print(self.buttonGroupValueType.checkedId())
        self.currentValueType = self.valueTypes[self.buttonGroupValueType.checkedId()]
        if self.currentValueType == "Expression":
            for q in self.quantityInputs:
                q.setVisible(False)
            for e in self.expressionInputs:
                e.setVisible(True)
        else:
            for q in self.quantityInputs:
                q.setVisible(True)
            for e in self.expressionInputs:
                e.setVisible(False)

    def constraintSettings(self):
        bcs = self.settings.copy()
        if self.currentValueType == "Expression":
            value = [e.text() for e in self.expressionInputs]
        else:
            value = [q.value() for q in self.quantityInputs]
        if self.numberOfComponents == 1:
            value = value[0]
        bcs["Value"] = value
        bcs["ValueType"] = self.currentValueType
        return bcs


if __name__ == "__main__":
    app = QApplication(sys.argv)
    _DefaultInitialTemperature = {
        "Name": "Temperature",
        "Symbol": "T",
        "Category": "InitialValue",
        "ValueType": "Quantity",
        "Unit": "K",
        "NumberOfComponents": 1,
        "Value": 300
    }
    _DefaultConstraintAcceleration = {
        "Name": "Acceleration",
        "Symbol": "g",
        "Category": "Source",
        "ValueType": "Quantity",
        "Unit": "m/s^2",
        "NumberOfComponents": 3,
        "Value": [0, 0, -9.8]
    }

    settings = _DefaultConstraintAcceleration
    dialog = ConstraintInputWidget(settings)
    dialog. show()
    app.exec_()
