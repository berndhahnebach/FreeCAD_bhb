#!/bin/bash

# Released under GPL v2.0
# bernd@bimstatik.org

# tested on Debian Jessie = 8.0
# packages installed by debian package manager apt-get
sudo apt-get install -y dictionaries-common

packages_build="\
    git                 \
    cmake               \
    g++                 \
    libboost-all-dev    \
    "
sudo apt-get install -y $packages_build

packages_lib="\
    doxygen             \
    libcoin80           \
    libcoin80-dev       \
    libeigen3-dev       \
    libpyside-dev       \
    libqtcore4          \
    libshiboken-dev     \
    libxerces-c-dev     \
    libxmu-dev          \
    libxmu-headers      \
    libxmu6             \
    libxmuu-dev         \
    libxmuu1            \
    libhdf5-dev         \
    libtogl-dev         \
    libfreetype6-dev    \
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
    "
sudo apt-get install -y $packages_div

packages_med="\
    libmed-dev          \
    libmedc-dev         \
    "
    #libmed              \
    #libmedc             \
sudo apt-get install -y $packages_med


# Netgen
sudo apt-get install -y automake  


# IfcOpenShell
sudo apt-get install -y libicu-dev
sudo apt-get install -y libghc-text-icu-dev


# OpenCascade
sudo apt-get install -y tcl8.5-dev tk8.5-dev


# free disk space by cleaning install files
sudo apt-get clean
