import socket
import threading
import pickle

class ChainReplicationNode:
    def __init__(self, host, port, next_node=None):
        self.host = host
        self.port = port
        self.next_node = next_node
        self.data = {}
        self.start()

    def start(self):
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Node running at {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    request = pickle.loads(data)

                    if request['action'] == 'get':
                        key = request['key']
                        if key in self.data:
                            conn.send(pickle.dumps(self.data[key]))
                        elif self.next_node:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as next_conn:
                                next_conn.connect((self.next_node.host, self.next_node.port))
                                next_conn.sendall(data)
                                result = next_conn.recv(1024)
                                conn.sendall(result)
                        else:
                            conn.send(b'Key not found')

                    elif request['action'] == 'put':
                        key = request['key']
                        value = request['value']
                        self.data[key] = value
                        conn.send(b'OK')

    def put(self, key, value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            request = {'action': 'put', 'key': key, 'value': value}
            client_socket.sendall(pickle.dumps(request))
            response = client_socket.recv(1024)
            print(response.decode())

    def get(self, key):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            request = {'action': 'get', 'key': key}
            client_socket.sendall(pickle.dumps(request))
            response = client_socket.recv(1024)
            # Load pickled data
            data = pickle.loads(response)
            print(data)

    def handle_node_failure(self):
        if self.next_node:
            self.next_node = self.next_node.next_node  # Skip the failed node

# Example usage
node3 = ChainReplicationNode('localhost', 6382)
node2 = ChainReplicationNode('localhost', 6381, next_node=node3)
node1 = ChainReplicationNode('localhost', 6380, next_node=node2)

# Simulate Node B failure
node2.handle_node_failure()

# Usage examples
node1.put('name', 'Alamin')
node1.get('name')