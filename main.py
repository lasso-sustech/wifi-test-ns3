#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from ns.core import CommandLine, Config
from ns.core import StringValue, Seconds
from ns.core import Simulator

import ns.wifi
from ns.applications import OnOffHelper

def main():
    pass

def build():
    
    pass

def run():
    # Simulator.Schedule( Seconds(1.0) )
    Simulator.stop( Seconds(44.0) )
    ##
    Simulator.Run()
    Simulator.Destroy()
    pass

if __name__=='__main__':
    try:
        args = CommandLine()
        args.parse(sys.argv)
        ##
        main(args)
    except Exception as e:
        raise e
    finally:
        pass
