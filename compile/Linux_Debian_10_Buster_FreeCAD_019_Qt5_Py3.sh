#!/bin/bash

# Released under GPL v2.0
# bernd@bimstatik.org
# Linux_Debian_09_Buster_compile_FreeCAD_no_externals_Qt5_Py3.sh

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
# get dependencies from distribution
packages_build="                \
    git                         \
    cmake                       \
    g++                         \
    libboost-all-dev            \
    "
sudo apt-get install -y $packages_build

packages_hard_dependencies="    \
    debhelper                   \
    dh-exec                     \
    dh-python                   \
    libcoin-dev                 \
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
    libpyside2-dev              \
    libqt5opengl5-desktop-dev   \
    libqt5svg5-dev              \
    libqt5webkit5-dev           \
    libqt5x11extras5-dev        \
    libqt5xmlpatterns5-dev      \
    libshiboken2-dev            \
    libspnav-dev                \
    libvtk6-dev                 \
    libx11-dev                  \
    libxerces-c-dev             \
    libzipios++-dev             \
    lsb-release                 \
    occt-draw                   \
    pyside2-tools               \
    python3-pyside2.qtcore      \
    python3-pyside2.qtgui       \
    python3-pyside2.qtsvg       \
    python3-pyside2.qtwidgets   \
    python3-pyside2uic          \
    python3-six                 \
    python3-yaml                \
    qtbase5-dev                 \
    qttools5-dev                \
    qtwebengine5-dev            \
    swig                        \
    "
sudo apt-get install -y $packages_hard_dependencies

packages_opt_dependencies="     \
    calculix-ccx                \
    gmsh                        \
    python3-matplotlib          \
    "
sudo apt-get install -y $packages_opt_dependencies

packages_pivy="           \
    libsimage-dev               \
    libsoqt520-dev              \
    python3-dbg                 \
    python3-numpy               \
    python3-setuptools          \
    python3-pyside2.qtopengl    \
    qt5-default                 \
    shiboken2                   \
    "
sudo apt-get install -y $packages_pivy
# pivy will be installed by a downloaded deb package, we need to install the dependencies manually


# *******************************************
# update and clean the system
sudo apt-get update
sudo apt-get clean


# *******************************************
# install pivy for Python3
cd $base_dir
wget https://github.com/berndhahnebach/FreeCAD_bhb/releases/download/1/python3-pivy_0.6.4-1_amd64.deb
sudo dpkg -i python3-pivy_0.6.4-1_amd64.deb


# *******************************************
# get FreeCAD latest Github commit
cd $base_dir
git clone https://github.com/FreeCAD/FreeCAD freecad


# *******************************************
# cmake, compile and install FreeCAD
mkdir build
cd build

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32286&start=40#p275718
cmake  -DBUILD_QT5=1  -DPYTHON_EXECUTABLE="/usr/bin/python3"  -DOCCT_CMAKE_FALLBACK=True  ../freecad
 
# https://forum.freecadweb.org/viewtopic.php?f=10&t=30340&start=190#p274393
# cmake                                                       \
# -DCMAKE_INSTALL_PREFIX:PATH=/opt/local/FreeCAD-0.18         \
#-DBUILD_QT5=ON                                              \
#-DCMAKE_BUILD_TYPE="DEBUG"                                  \
#-DFREECAD_BUILD_DEBIAN=ON                                   \
#-DOCC_INCLUDE_DIR="/usr/include/occt"                       \
#-DFREECAD_USE_OCCT_VARIANT="Official"                       \
#-DPYTHON_BASENAME=".cpython-37m-x86_64-linux-gnu"           \
#-DPYTHON_CONFIG_SUFFIX=".cpython-37m-x86_64-linux-gnu"      \
#-DPYTHON_EXECUTABLE="/usr/bin/python3.7"                    \
#../freecad

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32286#p269617
# -DBUILD_QT5=ON \

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32328#p269678
# -DOCCT_CMAKE_FALLBACK=True \
# I am not sure but I do think either above or the following is needed -DFREECAD_USE_OCCT_VARIANT="Official"

# https://forum.freecadweb.org/viewtopic.php?f=4&t=32286&start=20#p269806
# -DPYTHON_CONFIG_SUFFIX="-python2.7.x86_64-linux-gnu" \

make -j 2
sudo make install
sudo ln -s /opt/local/FreeCAD-0.18/bin/FreeCAD /usr/local/bin/FreeCAD  # make link
sudo ln -s /opt/local/FreeCAD-0.18/bin/FreeCADCmd /usr/local/bin/FreeCADCmd  # make link


# *******************************************
# run FreeCAD unit test
# FreeCADCmd --run-test 0  # all
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
