#!/usr/bin/env python

# External modules
from twisted.application import service, internet
from twisted.internet import main, interfaces, reactor
from zope.interface import implements
from socket import socket, AF_INET, SOCK_RAW, gethostbyname, gethostname, IPPROTO_RAW, SOL_IP, IP_HDRINCL
from scapy.all import TCP, IP, hexdump
import binascii
import struct

# Internal modules
from tun_factory import TUNFactory
from tun_reader import TUNPacketProducer, TUN_TestConsumer
from tun_writer import TUN_TestProducer
from nflog_reader import NFLogPacketProducer, NFLOG_TestConsumer
from tun_writer import TUNPacketConsumer
from hush_reader import HushPacketProducer
from hush_writer import HushPacketConsumer




def main():
    dest_ip       = '127.0.0.1'
    dest_port     = 6900

    tunFactory    = TUNFactory(remote_ip = '10.1.1.5',
                              local_ip  = '10.1.1.6',
                              netmask   = '255.255.255.0',
                              mtu       = 1500)
    tunDevice     = tunFactory.buildTUN()

    hush_consumer = HushPacketConsumer(dest_ip, dest_port)
    tun_producer  = TUNPacketProducer(tunDevice, hush_consumer) 

    tun_consumer  = TUNPacketConsumer(tunDevice)
    hush_producer = HushPacketProducer(consumer = tun_consumer)

    reactor.addWriter(tun_consumer) 
    reactor.addReader(tun_producer) 
    reactor.run()
    


if __name__ == '__main__':
    main()

