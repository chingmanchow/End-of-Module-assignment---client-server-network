import socket
import pickle
import base64

def start_server():
    # Initialize socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server started. Waiting for connections...")

    conn, addr = server_socket.accept()

    print(f"Connection received from {addr}")

    # Receive and deserialize dictionary from client
    data = conn.recv(1024)
    received_dict = pickle.loads(data)
    print(f"Received dictionary: {received_dict}")

    metadata =conn.recv(1024)
    decoded_metadata = pickle.loads(metadata)
    file_name = decoded_metadata['file_name']
    file_size = decoded_metadata['file_size']

    print(f"Receiving file: {file_name}")
    print(f"Expected file size: {file_size}")

    # Receiving the actual file data
    received_data = b""
    while len(received_data) < file_size:
        data = conn.recv(4096)  # Receive data in chunks
        if not data:
            # Connection might have been closed
            print("Connection closed before receiving complete data.")
            return

        received_data += data

    # Decoding the file data from base64
    file_data = base64.b64decode(received_data)

    # Save the file
    with open(file_name, 'wb') as file:
        file.write(file_data)

    print("File has been received and saved.")

    # #print contents of txt file
    # file_data = conn.recv(1024).decode()
    # print("file data: " + file_data)


    # # Open text file for reading the received content - server only needs to know that it is a txt file
    # with open('received_file.txt', 'rb') as f:
    #     content = f.read()
    #     print(f"File content:\n{content}")
    # print("File has been received.")

    conn.close()


if __name__ == "__main__":
    start_server()
