import netifaces as ni

def get_default_gateway():
    gateways = ni.gateways()
    gateway = gateways['default'][ni.AF_INET][0]
    print(f"default gateway: { gateway }")
    return gateway