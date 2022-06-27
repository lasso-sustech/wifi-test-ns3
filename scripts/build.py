#!/usr/bin/env python3
import os, sys
import psutil

NUM_JOBS = psutil.cpu_count() - 2
NS3_HOME = os.environ['NS3_HOME']

os.system( f'cp -rf ../src/* {NS3_HOME}/src' )
re_scan = ' '.join([x+'-apiscan' for x in os.listdir('../src')])

if sys.argv[1]=='--full':
    os.system( f'{NS3_HOME}/ns3 clean' )
    os.system( f'{NS3_HOME}/ns3 configure --enable-examples --enable-tests --enable-python-bindings --build-profile=optimized -- -DNS3_SCAN_PYTHON_BINDINGS=ON' )
    os.system( f'{NS3_HOME}/ns3 build {re_scan} -j{NUM_JOBS}' )
elif sys.argv[1]=='--fast':
    pass
else:
    pass

os.system( f'{NS3_HOME}/ns3 build -j{NUM_JOBS}' )
