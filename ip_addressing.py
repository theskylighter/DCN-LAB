import ipaddress

def subnet_details(ip_with_prefix):
    network = ipaddress.ip_network(ip_with_prefix, strict=False)
    
    print(f"IP Address: {ip_with_prefix}")
    print(f"Class: {determine_class(ip_with_prefix.split('/')[0])}")
    print(f"Subnet Mask: {network.netmask}")
    print(f"Network Address: {network.network_address}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"First Usable IP: {list(network.hosts())[0]}")
    print(f"Last Usable IP: {list(network.hosts())[-1]}")
    print(f"Number of Usable Hosts: {network.num_addresses - 2}")
    print(f"All Usable IPs: {list(network.hosts())}")

def determine_class(ip):
    first_octet = int(ip.split('.')[0])
    if first_octet < 128:
          return "Class A"
    elif first_octet < 192:
        return "Class B"
    elif first_octet < 224:
        return "Class C"
    elif first_octet < 240:
        return "Class D (Multicast)"
    else:
        return "Class E (Experimental)"

# Example usage
subnet_details("192.168.1.10/28")
