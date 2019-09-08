#!/bin/bash


base_dir=`pwd`

# building FreeCAD
cd $base_dir
cd freecad
mkdir build
cd build


# do not forget the backslash !!!
#cmake \
#-DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17  \
#-DFREECAD_USE_OCC_VARIANT="Official Version"  -DOCC_INCLUDE_DIR=/opt/local/FreeCAD-0.17/include/opencascade  -DOCC_LIBRARY=/opt/local/FreeCAD-0.17/lib/libTKernel.so \
#../freecad


sudo cmake \
-DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17  \
-DFREECAD_BUILD_DEBIAN=ON \
-DFREECAD_USE_OCC_VARIANT="Official Version"  \
-DOCC_INCLUDE_DIR=/opt/local/FreeCAD-0.17/include/opencascade  \
-DOCC_LIBRARY=/opt/local/FreeCAD-0.17/lib/libTKernel.so \
-DOCCT_CMAKE_FALLBACK=True \
../freecad

#https://forum.freecadweb.org/viewtopic.php?f=4&t=32328
#-DOCCT_CMAKE_FALLBACK=True \


make -j 2
sudo make install
sudo ln -s /opt/local/FreeCAD-0.17/bin/FreeCAD /usr/local/bin/FreeCAD  # make link
sudo ln -s /opt/local/FreeCAD-0.17/bin/FreeCADCmd /usr/local/bin/FreeCADCmd  # make link


# start FreeCAD
# cd ~
# /opt/local/FreeCAD-0.17/bin/FreeCAD
# 


# cmake options

# install directory
# -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.17  \

# -DBUILD_FEM_VTK=0  \

# -DBUILD_FEM_NETGEN=1  -DCMAKE_CXX_FLAGS="-DNETGEN_V5"  -DNETGEN_ROOT=/opt/local/FreeCAD-0.17  \

# if no oce-dev packages are installed
# -DOCC_INCLUDE_DIR=/opt/local/FreeCAD-0.17/include/opencascade  \ 

# if oce-dev packages are installed
# -DFREECAD_USE_OCC_VARIANT="Official Version"  -DOCC_INCLUDE_DIR=/opt/local/FreeCAD-0.17/include/opencascade  -DOCC_LIBRARY=/opt/local/FreeCAD-0.17/lib/libTKernel.so \
