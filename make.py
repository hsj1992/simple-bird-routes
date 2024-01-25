import os
import sys

def is_ipv6(cidr):
    return ':' in cidr

def has_english_chars(s):
    return any(char.isalpha() for char in s)

def process_txt_files(directory):
    ipv4_list = []
    ipv6_list = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line.startswith('#') and line:
                        cidr = line.split('#')[0].strip()  # Remove comments
                        if is_ipv6(cidr):
                            ipv6_list.append(cidr)
                        else:
                            ipv4_list.append(cidr)

    return ipv4_list, ipv6_list

def generate_routes_conf(ip_list, address):
    routes_conf = []
    for ip in ip_list:
        if has_english_chars(address) and ':' not in address:
            # English characters and no colon, assuming interface string
            routes_conf.append(f'route {ip} via "{address}";')
        elif not has_english_chars(address) and '.' in address:
            # No English characters and contains dot, assuming IPV4 address
            routes_conf.append(f'route {ip} via {address};')
        elif has_english_chars(address) and ':' in address:
            # English characters and contains colon, assuming IPV6 address
            routes_conf.append(f'route {ip} via {address};')
        else:
            # Default case, assuming interface string
            routes_conf.append(f'route {ip} via "{address}";')

    return routes_conf

def main():
    if len(sys.argv) != 3:
        print("Usage: python make.py <directory_path> <address>")
        sys.exit(1)

    directory_path = sys.argv[1]
    address = sys.argv[2]

    if os.path.isdir(directory_path):
        ipv4_list, ipv6_list = process_txt_files(directory_path)

        if ';' in address:
            # Assuming "IPV4;IPV6" format
            ipv4_address, ipv6_address = address.split(';')
            routes4_conf = generate_routes_conf(ipv4_list, ipv4_address)
            routes6_conf = generate_routes_conf(ipv6_list, ipv6_address)
        else:
            # Single address provided
            routes4_conf = generate_routes_conf(ipv4_list, address)
            routes6_conf = generate_routes_conf(ipv6_list, address)

        with open('routes4.conf', 'w') as file:
            file.write('\n'.join(routes4_conf))

        with open('routes6.conf', 'w') as file:
            file.write('\n'.join(routes6_conf))

        print("Static route configuration files (routes4.conf and routes6.conf) generated successfully.")
    else:
        print(f"The specified directory '{directory_path}' does not exist.")

if __name__ == "__main__":
    main()
