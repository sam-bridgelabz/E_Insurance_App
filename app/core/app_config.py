import os


def get_host_ip_address_n_port():
    host_ip_address = os.getenv("HOST_IP_ADDRESS", "127.0.0.1")  # default 127.0.0.1
    host_port_num = os.getenv("HOST_PORT_NUMBER", "8000")  # default 8000
    return host_ip_address, host_port_num
