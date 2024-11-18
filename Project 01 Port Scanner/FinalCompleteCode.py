from queue import Queue  # Import the Queue class from the queue module to handle the list of ports to scan
import socket  # Import the socket module to create and connect sockets
import threading  # Import the threading module to allow for multi-threaded execution

# Define the target IP address that will be scanned for open ports
target = "127.0.0.1"  # Loopback address for local testing

# Create a Queue object to hold the list of ports that need to be scanned
queue = Queue()

# Create a list to store open ports discovered during the scan
open_ports = []

def portscan(port):
    """
    Function to attempt a connection to a specific port on the target host.
    Returns True if the connection is successful (port is open), otherwise False.
    """
    try:
        # Create a socket object using IPv4 and TCP protocols
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Try to connect to the target host at the specified port
        sock.connect((target, port))
        
        # If connection is successful, return True indicating port is open
        return True
    except:
        # If any exception occurs (e.g., connection refused), return False indicating port is closed
        return False

def get_ports(mode):
    """
    Function to add ports to the queue based on the selected mode.
    Modes determine the range or specific ports to scan.
    """
    if mode == 1:
        # Mode 1: Scan ports 1 to 1023 (common well-known ports)
        for port in range(1, 1024):
            queue.put(port)  # Add each port to the queue
    elif mode == 2:
        # Mode 2: Scan ports 1 to 49151 (registered and dynamic/private ports)
        for port in range(1, 49152):
            queue.put(port)  # Add each port to the queue
    elif mode == 3:
        # Mode 3: Scan a predefined list of important ports
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)  # Add each port to the queue
    elif mode == 4:
        # Mode 4: Allow the user to enter custom ports to scan
        ports = input("Enter your ports (separated by blank):")
        
        # Split the user input into a list of strings and convert to integers
        ports = ports.split()
        ports = list(map(int, ports))
        
        # Add each port to the queue
        for port in ports:
            queue.put(port)

def worker():
    """
    Worker function to process the queue and perform port scans.
    Each thread runs this function to check ports in the queue.
    """
    while not queue.empty():
        # Get the next port from the queue
        port = queue.get()
        
        # Scan the port and check if it is open
        if portscan(port):
            # If the port is open, print the result and add it to the list of open ports
            print("Port {} is open!".format(port))
            open_ports.append(port)

def run_scanner(threads, mode):
    """
    Main function to set up and execute the port scanner with specified threads and mode.
    """
    # Populate the queue with ports based on the chosen mode
    get_ports(mode)

    # Create a list to hold the thread objects
    thread_list = []

    # Create and start the specified number of threads
    for t in range(threads):
        # Create a new thread that targets the worker function
        thread = threading.Thread(target=worker)
        
        # Add the thread to the list
        thread_list.append(thread)

    # Start each thread in the list
    for thread in thread_list:
        thread.start()

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()

    # After scanning, print all open ports that were found
    print("Open ports are:", open_ports)

# Run the port scanner with 200 threads and using mode 1 (scan ports 1 to 1024)
run_scanner(200, 1)
