#!/bin/bash

# Released under GPL v2.0
# bernd@bimstatik.org


# tested on Debian Buster = 10.0


#sudo rm -rf build_FC
#sudo rm -rf /opt/local/FreeCAD-0.17
mkdir build_FC
cd build_FC
base_dir=`pwd`
cd $base_dir


# *******************************************
echo START THE FreeCAD JOURNEY !!!
echo -----------------------------


# *******************************************
# update and upgrade system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
sudo apt-get update
sudo apt-get clean


# *******************************************
# get Dependencies from distribution
packages_build="\
    git                 \
    cmake               \
    g++                 \
    libboost-all-dev    \
    "
sudo apt-get install -y $packages_build

packages_hard_dependencies="\
    debhelper                   \
    dh-exec                     \
    dh-python                   \
    libcoin-dev               \
    libopencv-dev               \
    libeigen3-dev               \
    libgts-bin                  \
    libgts-dev                  \
    libkdtree++-dev             \
    libmedc-dev                 \
    libocct-data-exchange-dev   \
    libocct-ocaf-dev            \
    libocct-visualization-dev   \
    libproj-dev                 \
    libpyside-dev               \
    libqtcore4                  \
    libqtwebkit-dev             \
    libshiboken-dev             \
    libspnav-dev                \
    libvtk6-dev                 \
    libx11-dev                  \
    libxerces-c-dev             \
    libzipios++-dev             \
    lsb-release                 \
    occt-draw                   \
    pyside-tools                \
    python-dev                  \
    python-ply                  \
    qt4-dev-tools               \
    qt4-qmake                   \
    swig                        \
    "
sudo apt-get install -y $packages_hard_dependencies

packages_opt_dependencies="\
    python-matplotlib           \
    "
sudo apt-get install -y $packages_opt_dependencies

packages_div="\
    gmsh                \
    calculix-ccx        \
    "
sudo apt-get install -y $packages_div


# *******************************************
# update and clean the system
sudo apt-get update
sudo apt-get clean


# *******************************************
# get FreeCAD latest Github commit
cd $base_dir
git clone https://github.com/FreeCAD/FreeCAD -b releases/FreeCAD-0-18 freecad


# *******************************************
# cmake, compile and install FreeCAD
mkdir build
cd build
cmake \
-DFREECAD_BUILD_DEBIAN=ON \
-DPYTHON_CONFIG_SUFFIX="-python2.7.x86_64-linux-gnu" \
-DOCCT_CMAKE_FALLBACK=True \
../freecad

# -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.18  \
# -DOCC_INCLUDE_DIR="/usr/include/occt" \

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32328#p269678
# -DOCCT_CMAKE_FALLBACK=True \

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32286&start=20#p269806
# -DPYTHON_CONFIG_SUFFIX="-python2.7.x86_64-linux-gnu" \

make -j 2
sudo make install
sudo ln -s /opt/local/FreeCAD-0.18/bin/FreeCAD /usr/local/bin/FreeCAD  # make link
sudo ln -s /opt/local/FreeCAD-0.18/bin/FreeCADCmd /usr/local/bin/FreeCADCmd  # make link


# *******************************************
# run FreeCAD unit test
FreeCADCmd --run-test 0  # all
FreeCADCmd --run-test "TestFem"


# *******************************************
echo -----------------------------
echo END THE FreeCAD JOURNEY !!!


# *******************************************
# get back to bas dir
cd $base_dir


# *******************************************
# delete build_FC (all git clone and all build dirs)
cd ..
# sudo rm -rf build_FC
