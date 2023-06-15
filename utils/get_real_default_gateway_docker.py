import netifaces as ni

def get_real_default_gateway_docker():
    interfaces = ni.interfaces()
    print (interfaces)
    for interface in interfaces:
        if interface.startswith('eth'):
            iface_data = ni.ifaddresses(interface)
            print (iface_data)
            if ni.AF_INET in iface_data:
                for link in iface_data[ni.AF_INET]:
                    print (link)
                    if 'addr' in link:
                        print (link['addr'])
                        return link['addr']