#!/bin/bash

# Released under GPL v2.0
# bernd@bimstatik.org

# tested on Debian Stretch = 9.0
# packages installed by debian package manager apt-get
packages_build="\
    git                 \
    cmake               \
    g++                 \
    libboost-all-dev    \
    "
sudo apt-get install -y $packages_build

packages_lib="\
    doxygen             \
    libcoin80v5         \
    libcoin80-dev       \
    libeigen3-dev       \
    libfreetype6-dev    \
    libhdf5-dev         \
    libpyside-dev       \
    libqtcore4          \
    libshiboken-dev     \
    libtogl-dev         \
    libxerces-c-dev     \
    libxmu-dev          \
    libxmu-headers      \
    libxmu6             \
    libxmuu-dev         \
    libxmuu1            \
    libzipios++-dev     \
    "
sudo apt-get install -y $packages_lib

packages_dev="\
    qt4-dev-tools       \
    qt4-qmake           \
    libqtwebkit-dev     \
    cimg-dev            \
    petsc-dev           \
    tcl-dev             \
    "
sudo apt-get install -y $packages_dev

packages_python="\
    python-dev          \
    python-pyside       \
    python-matplotlib   \
    python-pivy         \
    pyside-tools        \
    "
sudo apt-get install -y $packages_python

packages_div="\
    swig                \
    shiboken            \
    gmsh                \
    calculix-ccx        \
    "
sudo apt-get install -y $packages_div


# Netgen
sudo apt-get install -y automake  


# IfcOpenShell
sudo apt-get install -y libicu-dev
sudo apt-get install -y libghc-text-icu-dev


# OpenCascade
sudo apt-get install -y tcl8.6-dev tk8.6-dev


# free disk space by cleaning install files
sudo apt-get clean
