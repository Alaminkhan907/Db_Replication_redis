import pickle
import socket

def get_value_from_node(address, port):
    # Create a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((address, port))
        # Send a command to request the value
        command = "GET_VALUE"
        client_socket.sendall(command.encode())
        # Receive the response
        response = client_socket.recv(1024)
        # Process the response
        value = pickle.loads(response)
        return value

# Main function
if __name__ == "__main__":
    node_address = 'localhost'
    node_port = 6382  # Assuming this is the port of the server you want to retrieve the value from
    value = get_value_from_node(node_address, node_port)
    print("Retrieved value:", value)