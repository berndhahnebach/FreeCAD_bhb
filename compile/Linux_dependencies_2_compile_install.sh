#!/bin/bash


base_dir=`pwd`


# building libMED
cd $base_dir
cd libmed
mkdir build
cd build
cmake ../libmed  -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17
make -j 2
sudo make install
cd ..
#rm -rf build


#  building VTK
cd $base_dir
cd vtk
mkdir build
cd build
cmake ../vtk   -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17 -DVTK_Group_Rendering:BOOL=OFF -DVTK_Group_StandAlone:BOOL=ON -DVTK_RENDERING_BACKEND=None
make -j 2
sudo make install
cd ..
#rm -rf build


# building OCCT
cd $base_dir
cd occt
mkdir build
cd build
cmake ../occt  -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17 -DUSE_VTK:BOOL=OFF
make -j 2
sudo make install
cd ..
#rm -rf build


# building IfcOpenShell
cd $base_dir
cd ifcopenshell
mkdir build
cd build
cmake ../ifcopenshell/cmake  -DOCC_INCLUDE_DIR=/opt/local/FreeCAD-0.17/include/opencascade  -DOCC_LIBRARY_DIR=/opt/local/FreeCAD-0.17/lib  -DPYTHON_INCLUDE_DIR=/usr/include/python2.7  -DPYTHON_LIBRARY=/usr/lib/python2.7/config-x86_64-linux-gnu/libpython2.7.so  -DUNICODE_SUPPORT=True  -DCOLLADA_SUPPORT=False  -DUSE_IFC4=False  -DBUILD_IFCPYTHON=True  -DBUILD_EXAMPLES=False
make -j 2
sudo make install  # installs to /usr/local !!!
cd ..
#rm -rf build


# get back to base dir
cd $base_dir
