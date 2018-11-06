# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2016 - FreeCAD                                 *
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

__title__ = "_ViewProviderFemConstraintAutoContact"
__author__ = "Michael Hindley"
__url__ = "http://www.freecadweb.org"

## @package ViewProviderFemConstraintSelfWeight
#  \ingroup FEM

import FreeCAD
import FreeCADGui
import FemGui  # needed to display the icons in TreeView
False if False else FemGui.__name__  # dummy usage of FemGui for flake8, just returns 'FemGui'

# for the panel
from femobjects import _FemConstraintAutoContact
from PySide import QtCore
from PySide import QtGui
# from femguiutils import selection_widgets

class _ViewProviderFemConstraintAutoContact:
    "A View Provider for the FemConstraintAutoContact object"
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        return ":/icons/FEM_ConstraintAutocontact.svg"

    def attach(self, vobj):
        from pivy import coin
        self.ViewObject = vobj
        self.Object = vobj.Object
        self.standard = coin.SoGroup()
        vobj.addDisplayMode(self.standard, "Default")
        
    def getDisplayModes(self, obj):
        return ["Default"]

    def getDefaultDisplayMode(self):
        return "Default"

    def updateData(self, obj, prop):
        return

    def onChanged(self, vobj, prop):
        return

    def setEdit(self, vobj, mode=0):
        # hide all meshes
        for o in FreeCAD.ActiveDocument.Objects:
            if o.isDerivedFrom("Fem::FemMeshObject"):
                o.ViewObject.hide()
        # show task panel
        taskd = _TaskPanelFemAutoContact(self.Object)
        taskd.obj = vobj.Object
        FreeCADGui.Control.showDialog(taskd)
        return True
    
    def unsetEdit(self, vobj, mode=0):
        FreeCADGui.Control.closeDialog()
        return True
    
    def doubleClicked(self, vobj):
        guidoc = FreeCADGui.getDocument(vobj.Object.Document)
        # check if another VP is in edit mode, https://forum.freecadweb.org/viewtopic.php?t=13077#p104702
        if not guidoc.getInEdit():
            guidoc.setEdit(vobj.Object.Name)
        else:
            from PySide.QtGui import QMessageBox
            message = 'Active Task Dialog found! Please close this one before open a new one!'
            QMessageBox.critical(None, "Error in tree view", message)
            FreeCAD.Console.PrintError(message + '\n')
        return True

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
    
class _TaskPanelFemAutoContact:
    '''The TaskPanel for editing References property of AutoContact objects'''

    def __init__(self, obj):

        self.obj = obj

        # parameter widget
        self.form = FreeCADGui.PySideUic.loadUi(FreeCAD.getHomePath() + "Mod/Fem/Resources/ui/AutoContact.ui") 
        QtCore.QObject.connect(self.form.btnAddContact, QtCore.SIGNAL("clicked()"), self.add_contact)
        QtCore.QObject.connect(self.form.btnRMContact, QtCore.SIGNAL("clicked()"), self.rm_contact)
        QtCore.QObject.connect(self.form.spSlope, QtCore.SIGNAL("valueChanged(int)"), self.set_slope) 
        QtCore.QObject.connect(self.form.spFriction, QtCore.SIGNAL("valueChanged(int)"), self.set_friction) 
        QtCore.QObject.connect(self.form.spFaceNum, QtCore.SIGNAL("valueChanged(int)"), self.set_face) 
        self.get_values()
               
    def accept(self):
        self.obj.slope = self.slope
        self.obj.friction = self.friction
        self.recompute_and_set_back_all()
        return True

    def reject(self):
        self.recompute_and_set_back_all()
        return True

    def recompute_and_set_back_all(self):
        doc = FreeCADGui.getDocument(self.obj.Document)
        doc.Document.recompute()
        doc.resetEdit()
        FreeCAD.ActiveDocument.removeObject("ConstraintAutoContact")
        
    def add_contact(self):
        from femtools import femutils
        femutils.AddAutoContact(self.slope,self.friction,self.facenum)

    def set_slope(self, base_quantity_value):
        self.slope = base_quantity_value
        
    def set_friction(self, base_quantity_value):
        self.friction = base_quantity_value
        
    def get_values(self):
        self.slope = self.obj.slope 
        self.friction= self.obj.friction
        self.facenum=self.obj.facenum
        
    def set_values(self):
        self.obj.slope = self.slope 
        self.obj.friction= self.friction
        self.obj.facenum=self.facenum
        
    def rm_contact(self):
        for obj in FreeCAD.ActiveDocument.Objects:
            if (obj.isDerivedFrom('Fem::ConstraintContact')):
                FreeCAD.ActiveDocument.removeObject(obj.Name)
        
    def set_face(self, base_quantity_value):
        self.facenum = base_quantity_value
