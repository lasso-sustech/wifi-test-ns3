#!/usr/bin/env python3
import sys
from ns.core import CommandLine, Config
from ns.core import StringValue, Seconds
from ns.core import Simulator
import visualizer

from ns.network import NodeContainer
from WLANTopology import BSSContainer

def main(args):
    build()
    run()
    pass

def build():
    ap_node = NodeContainer(); ap_node.Create(1)
    sta_nodes = NodeContainer(); sta_nodes.Create(2)
    BSSContainer('test-ap', ap_node, sta_nodes,
        standard='80211n', freq='2.4GHz', mcs='HtMcs7', channel=1, bw=20)
    pass

def run():
    visualizer.start()
    ##
    # Simulator.Schedule( Seconds(1.0) )
    # Simulator.stop( Seconds(44.0) )
    # #
    # Simulator.Run()
    # Simulator.Destroy()
    pass

if __name__=='__main__':
    try:
        args = CommandLine()
        args.Parse(sys.argv)
        ##
        main(args)
    except Exception as e:
        raise e
    finally:
        pass
