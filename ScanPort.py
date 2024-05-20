import socket
from concurrent.futures import ThreadPoolExecutor
import argparse

def scan_port(host, port):
    """
    Attempt to connect to the specified host on the specified port.
    Returns the port number if the connection is successful.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            return port
    except (socket.timeout, ConnectionRefusedError):
        return None

def scan_ports(host, start_port, end_port, max_threads):
    """
    Scan a range of ports on the specified host using a ThreadPoolExecutor.
    """
    with ThreadPoolExecutor(max_threads) as executor:
        ports = range(start_port, end_port + 1)
        results = list(executor.map(lambda port: scan_port(host, port), ports))
    
    open_ports = [port for port in results if port is not None]
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Simple Network Port Scanner")
    parser.add_argument("host", type=str, help="Host to scan")
    parser.add_argument("-sp", "--start-port", type=int, default=1, help="Starting port number (default: 1)")
    parser.add_argument("-ep", "--end-port", type=int, default=1024, help="Ending port number (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    
    args = parser.parse_args()
    
    print(f"Scanning {args.host} from port {args.start_port} to {args.end_port} using {args.threads} threads...")
    open_ports = scan_ports(args.host, args.start_port, args.end_port, args.threads)
    
    if open_ports:
        print(f"Open ports on {args.host}: {', '.join(map(str, open_ports))}")
    else:
        print(f"No open ports found on {args.host} in the range {args.start_port}-{args.end_port}.")

if __name__ == "__main__":
    main()
