import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
import requests

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

def print_local_ip():
    print("\n--- Device Local IP Information ---")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Local IP: {local_ip}")
    except Exception as e:
        print(f"Could not retrieve local IP: {e}")

def get_ip_info():
    url = 'https://ipinfo.io/json'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("\n--- Public IP Information ---")
            print(f"IP: {data.get('ip')}")
            print(f"Hostname: {data.get('hostname')}")
            print(f"City: {data.get('city')}")
            print(f"Region: {data.get('region')}")
            print(f"Country: {data.get('country')}")
            print(f"Location: {data.get('loc')}")
            print(f"Org: {data.get('org')}")
            print(f"Timezone: {data.get('timezone')}")
        else:
            print("Could not retrieve public IP info.")
    except Exception as e:
        print(f"Error fetching public IP info: {e}")

def ping(ip):
    command = ['ping', '-c', '1', '-W', '1', ip]
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL, universal_newlines=True)
        if 'ttl' in output.lower():
            return ip
    except Exception:
        pass
    return None

def scan_network():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        subnet = '.'.join(local_ip.split('.')[:3])
    except Exception:
        print("Could not determine local subnet.")
        return
    print(f"Scanning subnet: {subnet}.0/24...")
    ips = [f"{subnet}.{i}" for i in range(1, 255)]
    active_ips = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping, ips)
        for result in results:
            if result:
                active_ips.append(result)
    print("Active IP addresses:")
    for ip in active_ips:
        print(ip)

if __name__ == "__main__":
    print(ascii_banner)
    print_local_ip()
    get_ip_info()
    scan_network()