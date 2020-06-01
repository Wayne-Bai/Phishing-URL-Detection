import pyshark

cap = pyshark.FileCapture




class wireshark_analysis_script():

    # 此函数的作用是封装一下pyshark.FileCapture
    def read_packets_from_file(self, packets_file_path, tshark_path, display_filter):
        packets_file_obj = pyshark.FileCapture(input_file=packets_file_path, tshark_path=tshark_path,
                                               display_filter=display_filter)
        return packets_file_obj

    # 此函数的作用是从传送过来的所有数据包中，抽取并返回{ip_server,ip_client,port_server,port_client}四元组
    def get_target_client_ip_port(self, packets_file_obj):
        for tmp_packet in packets_file_obj:
            ip_server = tmp_packet.ip.src
            port_server = tmp_packet.tcp.srcport
            ip_client = tmp_packet.ip.dst
            port_client = tmp_packet.tcp.dstport
            yield {"ip_server": ip_server, "port_server": port_server, "ip_client": ip_client,
                   "port_client": port_client}

    # 此函数的作用是读取传过来的所有数据包应用层的数据，并打印
    def follow_tcp_stream(self, packets_file_obj, ip, port):
        for tmp_packet in packets_file_obj:
            highest_layer_name = tmp_packet.highest_layer
            if(tmp_packet.http.get_field('request.full.uri')):
                print(tmp_packet.http.get_field('request.full.uri'))
                data = tmp_packet.http.get_field('file_data')
                if ((tmp_packet.ip.dst == ip) and (tmp_packet.tcp.dstport == port)):
                    #print("server(%s:%s)->client(%s:%s): %s" % (tmp_packet.ip.src, tmp_packet.tcp.srcport, tmp_packet.ip.dst, tmp_packet.tcp.dstport,tmp_packet[highest_layer_name].get_field('data')))
                    print("server(%s:%s)->client(%s:%s): %s" % (tmp_packet.ip.src, tmp_packet.tcp.srcport, tmp_packet.ip.dst, tmp_packet.tcp.dstport,data))
                elif ((tmp_packet.ip.src == ip) and (tmp_packet.tcp.srcport == port)):
                    #print("client(%s:%s)->server(%s:%s): %s" % (tmp_packet.ip.src, tmp_packet.tcp.srcport, tmp_packet.ip.dst, tmp_packet.tcp.dstport,tmp_packet[highest_layer_name].get_field('data')))
                    print("client(%s:%s)->server(%s:%s): %s" % (tmp_packet.ip.src, tmp_packet.tcp.srcport, tmp_packet.ip.dst, tmp_packet.tcp.dstport,data))


if __name__ == '__main__':
    # 要读取的wireshark数据包的所在的路径
    packets_file_path = './caps/test3.pcapng'
    # tshark程序所在的路径，tshark随wireshark安装
    tshark_path = 'C:\\Program Files\\Wireshark\\tshark.exe'
    # 过滤器表达式，与在wireshark中使用时的写法完全相同
    first_step_filter = 'http.host==pertaminabiak.com'
    # 用于存放要追踪流的ip和端口
    target_client_ip_port = []

    # 实例化类
    wireshark_analysis_script_instance = wireshark_analysis_script()
    # 使用first_step_filter过滤器表达式，过滤出要追踪流的数据包
    first_step_obj = wireshark_analysis_script_instance.read_packets_from_file(packets_file_path, tshark_path,
                                                                               first_step_filter)
    # 从要追踪流的数据包中抽取出ip和端口
    target_client_ip_port = wireshark_analysis_script_instance.get_target_client_ip_port(first_step_obj)
    first_step_obj.close()
    # 遍历要追踪流的ip+端口组合
    for target_client_ip_port_temp in target_client_ip_port:
        ip_server = target_client_ip_port_temp['ip_server']
        port_server = target_client_ip_port_temp['port_server']
        ip_client = target_client_ip_port_temp['ip_client']
        port_client = target_client_ip_port_temp['port_client']
        # 这里是追踪流的关键，所有数据包中如果数据包中{ip_server,ip_client,port_server,port_client}四元组相同，那么就认为是同一个流
        # 当然追踪流一般都是追踪应用层的数据流，所以加上应用层协议运行过滤去掉三次握手四次挥手等没有应用层数据的数据包；我这里要追踪telnet数据流，所以除四元组外还加了telnet做过滤
        second_step_filter = 'http and ip.addr == %s and ip.addr == %s  and tcp.port == %s and tcp.port == %s' % (ip_server, ip_client, port_server, port_client)
        second_step_obj = wireshark_analysis_script_instance.read_packets_from_file(packets_file_path, tshark_path, second_step_filter)
        #print("[%s:%s]" % (ip_client, port_client))
        # 调用follow_tcp_stream将认为是同一个流的所有数据包的应用层数据打印
        wireshark_analysis_script_instance.follow_tcp_stream(second_step_obj, ip_client, port_client)
        second_step_obj.close()