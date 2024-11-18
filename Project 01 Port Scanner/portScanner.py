import socket

# target = "127.0.0.1" # for your own System
target = "127.0.0.1"

def portScanner(port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((target, port))
        return True
    except:
        return False
    
for port in range(1, 1024):

    result = portScanner(port)

    if result:
        print(f"Port {port} is Open!")
    else:
        print(f"Port {port} is Closed!")

print(portScanner(8080))