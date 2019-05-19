#!/bin/bash

# Released under GPL v2.0
# bernd@bimstatik.org


# *******************************************
# update and upgrade system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
sudo apt-get update
sudo apt-get clean


# *******************************************
# FreeCAD
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
    python-dev                  \
    python-ply                  \
    qt4-dev-tools               \
    qt4-qmake                   \
    swig                        \
    "

sudo apt-get install -y $packages_hard_dependencies

# nicht on buster
#    pyside-tools                \
#     libpyside-dev               \


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
# Netgen
sudo apt-get install -y automake  


# *******************************************
# IfcOpenShell
sudo apt-get install -y libicu-dev
sudo apt-get install -y libghc-text-icu-dev


# *******************************************
# OpenCascade
sudo apt-get install -y tcl8.6-dev tk8.6-dev


# *******************************************
# free disk space by cleaning install files
sudo apt-get clean
