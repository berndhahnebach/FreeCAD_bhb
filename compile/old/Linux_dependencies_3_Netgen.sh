 
#!/bin/bash


# building Netgen 5.3.1
cd $base_dir
cd netgen
cd netgen/netgen-5.3.1
./configure --prefix=/opt/local/FreeCAD-0.17 --with-tcl=/usr/lib/tcl8.5 --with-tk=/usr/lib/tk8.5  --enable-occ --with-occ=/opt/local/FreeCAD-0.17 --enable-shared --enable-nglib CXXFLAGS="-DNGLIB_EXPORTS -std=gnu++11"
make -j 2
sudo make install
# copy libsrc, FreeCAD needs it
cd $base_dir
cd netgen
sudo cp -rf netgen/netgen-5.3.1/libsrc  /opt/local/FreeCAD-0.17/libsrc
cd ..
rm -rf build




##############################################
# get netgen 6.3
# cd $base_dir
# rm -rf * netgen
# mkdir netgen
# cd netgen
# git clone https://github.com/looooo/netgen netgen
# tar cvfj netgen.tar.bz2 netgen/
# chown vagrant.vagrant netgen.tar.bz2
# mv netgen.tar.bz2 ..


# building Netgen 6.3
#cd $base_dir
#cd netgen
#./configure  --prefix=/opt/local/FreeCAD-0.17  --with-tcl=/usr/lib/tcl8.5  --with-tk=/usr/lib/tk8.5  --enable-occ --with-occ=/opt/local/FreeCAD-0.17  --enable-shared  --enable-nglib CXXFLAGS="-DNGLIB_EXPORTS -std=gnu++11"
#mkdir build
#cd build
#cmake ../netgen
#make -j 2
#sudo make install


# copy libsrc, FreeCAD needs it
# cd $base_dir
#cd netgen
#sudo cp -rf netgen/netgen-5.3.1/libsrc  /opt/local/FreeCAD-0.17/libsrc
#cd ..
#rm -rf build
