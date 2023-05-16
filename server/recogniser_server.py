from intellichess.recognition.recognition import ChessRecognizer
import numpy as np
import socket
import json
import chess
import traceback
import cv2
from recap import URI

# Define the server address and port
SERVER_ADDRESS = '95.179.202.254'
SERVER_PORT = 5555

recogniser = ChessRecognizer(URI('models://transfer_learning'))

# Create a socket object
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # Bind the socket to a specific address and port
# server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
# server_socket.listen(1)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
    while True:
        s.listen()
        print('Waiting for a client to connect...')
        conn, addr = s.accept()
        print(f'Client connected: {addr}')

        # Receive the image bytes from the client
        with conn:
            data = b''
            while True:
                chunk = conn.recv(1024)
                print(chunk)
                if not chunk:
                    break
                data += chunk
                if data.endswith(b"END"):
                    break

            # if not data:
            #     # If the client has closed the connection, break out of the loop
            #     break

            # Convert binary data to NumPy array
            try:
                img_data = np.frombuffer(data, dtype=np.uint8)
                img_np = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                print(f'Received message with shape: {img_data.shape}')
                board, corners = recogniser.predict(img_np, chess.WHITE)
                print(board)

                response = {'message': board.board_fen()}
                response_json = json.dumps(response)

                # Send the response back to the client
                conn.send(response_json.encode())
            except Exception as e:
                print(traceback.format_exc())
        # Close the client connection
        conn.close()
        print(f'Client disconnected: {addr}')

# Close the server socket
#server_socket.close()