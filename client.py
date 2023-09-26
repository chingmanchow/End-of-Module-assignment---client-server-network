# import socket
# import pickle
# import os
# import base64


# def start_client():
#     # Initialize socket
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Try to establish a connection
#     try:
#         client_socket.connect(('localhost', 12345))
#     except socket.error as e:
#         print(f"Error occurred while connecting: {e}")
#         return

#     # Create and populate a dictionary
#     data_dict = {'name': 'Christine', 'age': 35, 'city': 'London'}

#     # Serialize the dictionary
#     serialized_data = pickle.dumps(data_dict)

#     # Try to send the serialized dictionary to the server
#     try:
#         client_socket.sendall(serialized_data)
#     except socket.error as e:
#         print(f"Error occurred while sending data: {e}")
#         return

#     print("Dictionary has been sent")

#     # Prepare the text file
#     file_name = 'sample_file.txt'

#     if not os.path.isfile(file_name):
#         print(f"File {file_name} does not exist.")
#         return

#     with open(file_name, 'rb') as f:
#         file_data = f.read()

#     # Encode the file data
#     encoded_file_data = base64.b64encode(file_data)

#     # Get the size of the encoded file data
#     size = len(encoded_file_data)

#     # Try to transmit file name and size to the receiver
#     try:
#         client_socket.send(pickle.dumps({'file_name': file_name, 'file_size': size}))
#     except socket.error as e:
#         print(f"Error occurred while sending file metadata: {e}")
#         return

#     # Try to send the encoded file data
#     try:
#         client_socket.sendall(encoded_file_data)
#     except socket.error as e:
#         print(f"Error occurred while sending file data: {e}")
#         return

#     print("File has been sent.")

#     client_socket.close()


# if __name__ == "__main__":
#     start_client()

import socket
import pickle
import os
import base64
import time


def start_client():
    # Initialize socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to establish a connection
    try:
        client_socket.connect(('localhost', 12345))
    except socket.error as e:
        print(f"Error occurred while connecting: {e}")
        return

    # Create and populate a dictionary
    data_dict = {'name': 'Christine', 'age': 35, 'city': 'London'}

    # Serialize the dictionary
    serialized_data = pickle.dumps(data_dict)

    # Try to send the serialized dictionary to the server
    max_retries = 5
    for i in range(max_retries):
        try:
            client_socket.sendall(serialized_data)
            print("Dictionary has been sent")
            break
        except socket.error as e:
            if i < max_retries - 1:  # i is zero indexed
                time.sleep(1)  # wait a bit before trying again
                continue
            else:
                print(f"Error occurred while sending data: {e}")
                return

    # Prepare the text file
    file_name = 'sample_file.txt'
    if not os.path.isfile(file_name):
        print(f"File {file_name} does not exist.")
        return

    with open(file_name, 'rb') as f:
        file_data = f.read()

    # Encode the file data
    encoded_file_data = base64.b64encode(file_data)

    # Get the size of the encoded file data
    size = len(encoded_file_data)

    # Try to transmit file name and size to the receiver
    for i in range(max_retries):
        try:
            client_socket.send(pickle.dumps({'file_name': file_name, 'file_size': size}))
            break
        except socket.error as e:
            if i < max_retries - 1:  # i is zero indexed
                time.sleep(1)  # wait a bit before trying again
                continue
            else:
                print(f"Error occurred while sending file metadata: {e}")
                return

    # Try to send the encoded file data
    for i in range(max_retries):
        try:
            client_socket.sendall(encoded_file_data)
            print("File has been sent.")
            break
        except socket.error as e:
            if i < max_retries - 1:  # i is zero indexed
                time.sleep(1)  # wait a bit before trying again
                continue
            else:
                print(f"Error occurred while sending file data: {e}")
                return

    client_socket.close()


if __name__ == "__main__":
    start_client()
