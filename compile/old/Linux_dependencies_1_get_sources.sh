#!/bin/bash


base_dir=`pwd`


# get MED
cd $base_dir
mkdir libmed
cd libmed
git clone https://github.com/berndhahnebach/libMED.git libmed
#tar cvfj libmed.tar.bz2 libmed/
#chown vagrant.vagrant libmed.tar.bz2
#mv libmed.tar.bz2 ..


# get VTK 8.1.0
cd $base_dir
mkdir vtk
cd vtk
wget https://www.vtk.org/files/release/8.1/VTK-8.1.0.tar.gz
gunzip VTK-8.1.0.tar.gz
tar xf VTK-8.1.0.tar
rm VTK-8.1.0.tar
mv VTK-8.1.0 vtk
#tar cvfj vtk.tar.bz2 vtk/
#chown vagrant.vagrant vtk.tar.bz2
#mv vtk.tar.bz2 ..


# get OCCT 7.2.0
cd $base_dir
mkdir occt
cd occt
wget "http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=8e8645100f6b47000e40bb41e644ae2590400193;sf=tgz"
mv "index.html?p=occt.git;a=snapshot;h=8e8645100f6b47000e40bb41e644ae2590400193;sf=tgz" occt.tgz
gunzip occt.tgz
tar xf occt.tar
rm occt.tar
mv occt-8e86451 occt
cd occt
grep -v vtkRenderingFreeTypeOpenGL src/TKIVtk/EXTERNLIB >& /tmp/EXTERNLIB
\cp /tmp/EXTERNLIB src/TKIVtk/EXTERNLIB
grep -v vtkRenderingFreeTypeOpenGL src/TKIVtkDraw/EXTERNLIB >& /tmp/EXTERNLIB
\cp /tmp/EXTERNLIB src/TKIVtkDraw/EXTERNLIB
#cd ..
#tar cvfj occt.tar.bz2 occt/
#chown vagrant.vagrant occt.tar.bz2
#mv occt.tar.bz2 ..


# get Netgen 5.3.1
cd $base_dir
mkdir netgen
cd netgen
git clone https://github.com/berndhahnebach/Netgen netgen
#tar cvfj netgen.tar.bz2 netgen/
#chown vagrant.vagrant netgen.tar.bz2
#mv netgen.tar.bz2 ..


# get IfcOpenShell
cd $base_dir
mkdir ifcopenshell
cd ifcopenshell
git clone https://github.com/IfcOpenShell/IfcOpenShell ifcopenshell
#tar cvfj ifcopenshell.tar.bz2 ifcopenshell/
#chown vagrant.vagrant ifcopenshell.tar.bz2
#mv ifcopenshell.tar.bz2 ..


# get FreeCAD latest Github commit
cd $base_dir
mkdir freecad
cd freecad
git clone https://github.com/FreeCAD/FreeCAD -b releases/FreeCAD-0-18 freecad
#tar cvfj freecad.tar.bz2 freecad/
#chown vagrant.vagrant freecad.tar.bz2
#mv freecad.tar.bz2 ..


# go back to base dir
cd $base_dir


# $ vagrant plugin install vagrant-scp
# https://medium.com/@smartsplash/using-scp-and-vagrant-scp-in-virtualbox-to-copy-from-guest-vm-to-host-os-and-vice-versa-9d2c828b6197
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/libmed.tar.bz2 libmed.tar.bz2
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/vtk.tar.bz2 vtk.tar.bz2
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/occt.tar.bz2 occt.tar.bz2
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/netgen.tar.bz2 netgen.tar.bz2
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/ifcopenshell.tar.bz2 ifcopenshell.tar.bz2
# vagrant scp :/home/vagrant/Documents/build_FreeCAD/freecad.tar.bz2 freecad.tar.bz2
