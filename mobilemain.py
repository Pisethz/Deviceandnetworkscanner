import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
import requests
import psutil

# ASCII art banner with project name and authors
ascii_banner = r'''
 _____                _             _____                _             _   _                _   
(___  )              ( )           (___  )              ( )           ( ) ( )              ( )_ 
    | |   _ _    ___ | |/')  _   _     | |   _ _    ___ | |/')  _   _ | |_| | _   _   ___  | ,_)
 _  | | /'_` ) /'___)| , <  ( ) ( ) _  | | /'_` ) /'___)| , <  ( ) ( )|  _  |( ) ( )/' _ `\| |  
( )_| |( (_| |( (___ | |\`\ | (_) |( )_| |( (_| |( (___ | |\`\ | (_) || | | || (_) || ( ) || |_ 
`\___/'`\__,_)`\____)(_) (_)`\__, |`\___/'`\__,_)`\____)(_) (_)`\__, |(_) (_)`\___/'(_) (_)`\__)
                            ( )_| |                            ( )_| |                          
                            `\___/'                            `\___/'                          

Pisethz x JackyJackyHunt
'''

# Removed tkinter and ascii art banner

def print_and_collect(text, output):
    print(text)
    output.append(text)

def print_all_network_info(output):
    print_and_collect("\n--- Windows IP Configuration (All Network Adapters) ---", output)
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for iface, addr_list in addrs.items():
        print_and_collect(f"\nAdapter: {iface}", output)
        if iface in stats:
            stat = stats[iface]
            print_and_collect(f"  Status: {'Up' if stat.isup else 'Down'}", output)
            print_and_collect(f"  MTU: {stat.mtu}", output)
            print_and_collect(f"  Speed: {stat.speed} Mbps" if stat.speed else "  Speed: Unknown", output)
        mac = None
        for addr in addr_list:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
                print_and_collect(f"  Physical Address (MAC): {mac}", output)
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                print_and_collect(f"  IPv4 Address: {addr.address}", output)
                print_and_collect(f"    Netmask: {addr.netmask}", output)
                print_and_collect(f"    Broadcast: {addr.broadcast}", output)
            elif addr.family == socket.AF_INET6:
                print_and_collect(f"  IPv6 Address: {addr.address}", output)
                print_and_collect(f"    Netmask: {addr.netmask}", output)
                print_and_collect(f"    Broadcast: {addr.broadcast}", output)

def print_local_ip(output):
    print_and_collect("\n--- Device Local IP Information ---", output)
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print_and_collect(f"Local IP: {local_ip}", output)
    except Exception as e:
        print_and_collect(f"Could not retrieve local IP: {e}", output)

def get_ip_info(ip_version='ipv4'):
    if ip_version == 'ipv4':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/json'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print(f"Error fetching {ip_version} info: {e}")
    return None

def print_ip_info(output):
    print_and_collect("\n--- Public IP Information ---", output)
    info = get_ip_info('ipv4')
    if info:
        print_and_collect(f"IP: {info.get('ip')}", output)
        print_and_collect(f"Hostname: {info.get('hostname')}", output)
        print_and_collect(f"City: {info.get('city')}", output)
        print_and_collect(f"Region: {info.get('region')}", output)
        print_and_collect(f"Country: {info.get('country')}", output)
        print_and_collect(f"Location: {info.get('loc')}", output)
        print_and_collect(f"Org: {info.get('org')}", output)
        print_and_collect(f"Timezone: {info.get('timezone')}", output)
    else:
        print_and_collect("Could not retrieve public IP info.", output)

def ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', ip]
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL, universal_newlines=True)
        if 'ttl' in output.lower():
            return ip
    except Exception:
        pass
    return None

def scan_network(output):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = '.'.join(local_ip.split('.')[:3])
    print_and_collect(f"Scanning subnet: {subnet}.0/24...", output)
    ips = [f"{subnet}.{i}" for i in range(1, 255)]
    active_ips = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(ping, ips)
        for result in results:
            if result:
                active_ips.append(result)
    print_and_collect("Active IP addresses:", output)
    for ip in active_ips:
        print_and_collect(ip, output)

if __name__ == "__main__":
    print(ascii_banner)
    output = []
    print_all_network_info(output)
    print_local_ip(output)
    print_ip_info(output)
    scan_network(output)
    # Print all results to CLI
    # (Already printed in print_and_collect)
