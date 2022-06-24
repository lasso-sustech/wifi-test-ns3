#!/usr/bin/env python3
#https://www.nsnam.org/docs/models/html/wifi-user.html

from ns.core import (StringValue, BooleanValue, UintegerValue)
from ns.internet import InternetStackHelper, Ipv4AddressHelper
from ns.network import Ipv4Address, Ipv4Mask
# from ns.mobility import MobilityHelper

from ns.wifi import (WIFI_STANDARD_80211n, WIFI_STANDARD_80211ac, WIFI_STANDARD_80211ax)
from ns.wifi import YansWifiPhyHelper, YansWifiChannelHelper
from ns.wifi import WifiMacHelper, Ssid, SsidValue
from ns.wifi import WifiHelper

global GROUP_INDEX
GROUP_INDEX = 1
GLOBAL_PHY = dict()
CHANNEL_MAP = {
    '2.4GHz': {
        20: range(1,15), #[1,2,...,14]
    },
    '5GHz': {
        20:  [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 161, 165, 169],
        40:  [38, 46, 54, 62, 102, 110, 118, 126, 134, 142, 151, 159],
        80:  [42, 58, 106, 122, 138, 155],
        160: [50, 114],
    },
    '6GHz': { #for 802.11ax only
        20: [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 129, 133, 137, 141, 145, 149, 153, 157, 161, 165, 169, 173, 177, 181, 185, 189, 193, 197, 201, 205, 209, 213, 217, 221, 225, 229, 233],
        40: [3, 11, 19, 27, 35, 43, 51, 59, 67, 75, 83, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171, 179, 187, 195, 203, 211, 219, 227],
        80: [7, 23, 39, 55, 71, 87, 103, 119, 135, 151, 167, 183, 199, 215],
        160: [15, 47, 79, 111, 143, 175, 207],
    }
}

def get_wifi_phy(freq, bw, channel):
    assert( freq in ['2.4GHz', '5GHz', '6GHz'] )
    assert( channel in CHANNEL_MAP[freq][bw] )
    ##
    freq = {'2.4GHz':'2_4GHZ', '5GHz':'5GHZ', '6GHz':'6GHZ'}[freq]
    freq_name = f'BAND_{freq}'
    phy_name  = f'{{{channel}, 0, {freq_name}, 0}}'
    ##
    if phy_name in GLOBAL_PHY:
        wifiPhy = None
    else:
        wifiPhy = YansWifiPhyHelper()
        wifiPhy.Set('Antennas', UintegerValue(2))
        wifiPhy.Set('MaxSupportedTxSpatialStreams', UintegerValue(2))
        wifiPhy.Set('MaxSupportedRxSpatialStreams', UintegerValue(2))
        wifiPhy.Set('ChannelSettings', StringValue(phy_name) )
        #
        GLOBAL_PHY[phy_name] = wifiPhy
        wifiChannel = YansWifiChannelHelper.Default()
        wifiPhy.SetChannel( wifiChannel.Create() )
    return wifiPhy

class WLANTopology:
    def __init__(self, standard='80211n', freq='2.4GHz', channel=1, bw=20):
        global GROUP_INDEX
        assert( standard in ['80211n', '80211a', '80211ac', '80211ax'] )
        assert( standard=='80211ax' if freq=='6GHz' else True )
        assert( freq=='5GHz' if standard=='80211a' else True )
        ##
        _standard = {
            '80211n' : WIFI_STANDARD_80211n,
            '80211ac': WIFI_STANDARD_80211ac,
            '80211ax': WIFI_STANDARD_80211ax
        }[standard]
        self.wifi = WifiHelper()
        self.wifi.SetStandard(_standard)
        ##
        self.id = GROUP_INDEX
        GROUP_INDEX += 1
        ##
        self.nodes = list()
        self.devs = list()
        pass

    def install_stacks(self):
        stack = InternetStackHelper()
        [ stack.Install(nd) for nd in self.nodes ]
        ##
        _id = self.id
        self.ifaces = list()

        address = Ipv4AddressHelper()
        address.SetBase(
            Ipv4Address(f'10.1.{_id}.0'), Ipv4Mask('255.255.255.0') )
        for dev in self.devs:
            self.ifaces.append( address.Assign(dev) )
        [ address.Assign(dev) for dev in self.devs ]
        pass

    pass

class BSSContainer(WLANTopology):
    def __init__(self, ssid, ap_node, sta_nodes,
            standard='80211n', freq='2.4GHz', channel=1, bw=20):
        super().__init__(standard, freq, channel, bw)
        #
        wifiPhy = get_wifi_phy(freq, bw, channel)
        wifiMac = WifiMacHelper()
        #
        wifiMac.SetType( 'ns3::ApWifiMac', 'Ssid', SsidValue(Ssid(ssid)),
            'QosSupported', BooleanValue (True) )
        self.ap_node = ap_node
        self.ap_dev  = self.wifi.Install(wifiPhy, wifiMac, ap_node)
        #
        wifiMac.SetType( 'ns3::StaWifiMac', 'Ssid', SsidValue(Ssid(ssid)),
            'ActiveProbing', BooleanValue(False) )
        self.sta_nodes = sta_nodes
        self.sta_devs = self.wifi.Install(wifiPhy, wifiMac, sta_nodes)
        ##
        self.nodes = [self.ap_node, self.sta_nodes]
        self.devs  = [self.ap_dev, self.sta_devs]
        self.install_stacks()
        self.ap_iface, self.sta_ifaces = self.ifaces
        pass

    pass

class P2PContainer(WLANTopology):
    pass
