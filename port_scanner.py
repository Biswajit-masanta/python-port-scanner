import socket
from datetime import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# ==========================
# TARGET VALIDATION
# ==========================

target = input("Enter IP Address to Scan: ")

try:
    socket.gethostbyname(target)
except socket.gaierror:
    print(Fore.RED + "[!] Invalid Host")
    exit()

# ==========================
# PORT RANGE VALIDATION
# ==========================

try:
    start_port = int(input("Starting Port: "))
    end_port = int(input("Ending Port: "))
except ValueError:
    print(Fore.RED + "[!] Invalid Port Number")
    exit()

if start_port < 1 or end_port > 65535:
    print(Fore.RED + "[!] Ports must be between 1 and 65535")
    exit()

if start_port > end_port:
    print(Fore.RED + "[!] Starting port cannot be greater than ending port")
    exit()

# ==========================
# SCAN START
# ==========================

print("\n" + "=" * 50)
print("          PYTHON PORT SCANNER")
print("=" * 50)

print(f"Target      : {target}")
print(f"Port Range  : {start_port}-{end_port}")
print("-" * 50)

open_ports = []
start_time = datetime.now()

# ==========================
# PORT SCANNING
# ==========================

for port in range(start_port, end_port + 1):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    result = s.connect_ex((target, port))

    if result == 0:

        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown"

        open_ports.append((port, service))

        print(
            Fore.GREEN +
            f"[OPEN] Port {port:<5} | Service: {service}"
        )

    s.close()

# ==========================
# SCAN SUMMARY
# ==========================

end_time = datetime.now()

print("\n" + "=" * 50)
print("            SCAN SUMMARY")
print("=" * 50)

print(f"Target           : {target}")
print(f"Total Open Ports : {len(open_ports)}")
print(f"Scan Duration    : {end_time - start_time}")

if open_ports:
    print("\nOpen Ports Found:")

    for port, service in open_ports:
        print(
            Fore.YELLOW +
            f"  -> Port {port:<5} ({service})"
        )
else:
    print(Fore.RED + "\nNo open ports found.")