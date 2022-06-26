#!/usr/bin/bash
CPU_CORES=`grep -c ^processor /proc/cpuinfo`
JOBS=$(( $CPU_CORES - 2 ))

cp -rf ../src/* $NS3_HOME/src
$NS3_HOME/ns3 build -j$JOBS
