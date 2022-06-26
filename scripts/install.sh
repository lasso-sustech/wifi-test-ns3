#!/usr/bin/bash
NS3=ns-3.36.1
CPU_CORES=`grep -c ^processor /proc/cpuinfo`
JOBS=$(( $CPU_CORES - 2 ))

## https://www.nsnam.org/wiki/Installation
# Install "NS3 Python API" dependencies
sudo apt install git g++ python3 python3-dev pkg-config python3-setuptools sqlite3 libsqlite3-dev cmake -y
# Install "ns-3-pyviz visualizer" dependencies
sudo apt install gir1.2-goocanvas-2.0 python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython3 -y
# Install "bake build tool" dependencies
sudo apt install autoconf cvs bzr unrar -y
# Install "GNU Scientific Library (GSL) support" dependencies
sudo apt install gsl-bin libgsl-dev libgslcblas0 -y

## prepare Bake.py and envrionment variables
mkdir -p $HOME/build
git clone https://gitlab.com/nsnam/bake $HOME/build/bake --depth=1
##
echo '''
export BAKE_HOME=$HOME/build/bake
export PATH=$PATH:$BAKE_HOME
export PYTHONPATH=$PYTHONPATH:$BAKE_HOME
''' > $HOME/.ns3-bake.sh
echo 'export NS3_HOME=$BAKE_HOME/source/${NS3}' >> $HOME/.ns3-bake.sh
echo '''export PATH=$PATH:$NS3_HOME
export PYTHONPATH=$PYTHONPATH:$NS3_HOME/build/bindings/python
''' >> $HOME/.ns3-bake.sh
##
source $HOME/.ns3-bake.sh

## download ns3 with Bake.py
cd $BAKE_HOME && $BAKE_HOME/bake.py check
cd $BAKE_HOME && $BAKE_HOME/bake.py configure -e ${NS3}
cd $BAKE_HOME && bake.py download
# $BAKE_HOME/bake.py build -j$JOBS
# build ns3 with python-bindings enabled
$NS3_HOME/ns3 configure --enable-examples --enable-tests --enable-python-bindings --build-profile=optimized
$NS3_HOME/ns3 build -j$JOBS
