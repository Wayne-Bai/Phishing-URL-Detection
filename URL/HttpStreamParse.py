#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019/9/10

@Author : leizhang
"""
import pyshark as pk
import datetime

class HttpStreamParse():
    def __init__(self):
        pass

    def ReadPcap(self, packet_path, tshark_path, display_filter):
        #cap = pk.FileCapture(input_file=packet_path, display_filter=display_filter)
        cap = pk.FileCapture(input_file=packet_path, tshark_path=tshark_path, display_filter=display_filter)
        return cap

    def FollowTcpStream(self, tshark_path,display_filter):
        cap = hsp.ReadPcap(pcap, tshark_path, display_filter)
        for packet in cap:
            stream_info = {}
            if packet.highest_layer != 'TCP'and packet.highest_layer != 'DATA':
                stream_info['src_ip'] = packet.ip.src
                stream_info['src_port'] = packet.tcp.srcport
                stream_info['dst_ip'] = packet.ip.dst
                stream_info['dst_port'] = packet.tcp.dstport
                stream_info['highest_layer'] = packet.highest_layer
                print('%s:%s ---> %s:%s %s' % (stream_info['src_ip'], stream_info['src_port'],
                                               stream_info['dst_ip'], stream_info['dst_port'],
                                               stream_info['highest_layer']))
                if hasattr(packet.http, 'request'):
                    stream_info['full_uri'] = packet.http.request_full_uri
                    print('request_full_uri: %s' % stream_info['full_uri'])
                elif hasattr(packet.http, 'response'):
                    stream_info['response_for_uri'] = packet.http.response_for_uri
                    print('response_for_uri: %s' % stream_info['response_for_uri'])
                    if 'text/html' in packet.http.content_type:
                        print('text/html')
                        html = ''.join(packet[packet.highest_layer]._get_all_field_lines())
                        # html.replace('\\n', '').replace('\\r', '')
                        time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                        file_name = 'resource/%s.txt' % time
                        with open(file_name, 'w') as f:
                            f.write(stream_info['response_for_uri'] + '\n' + html)
                    elif packet.highest_layer == 'image/jpeg':
                        print('image/jpeg')
                    elif packet.http.content_type == 'text/css':
                        print('text/css')
                    elif packet.http.content_type == 'application/javascript':
                        print('application/javascript')
            else:
                pass


if __name__ == '__main__':
    tshark_path = 'C:\\Program Files\\Wireshark\\tshark.exe'
    pcap = "./caps/test3.pcapng"
    #display_filter_1 = "http and http.request"
    display_filter_1 = "http.host==pertaminabiak.com"
    hsp = HttpStreamParse()
    cap = hsp.ReadPcap(pcap, tshark_path,display_filter_1)
    stream_index_list = []

    for packet in cap:
        stream_index = packet.tcp.stream
        if stream_index_list.count(stream_index) == 0:
            print('\n[stream_index: %s]' % stream_index)
            display_filter_2 = 'tcp.stream eq %s' % stream_index
            hsp.FollowTcpStream(tshark_path,display_filter_2)
        stream_index_list.append(stream_index)
