from intellichess.recognition.recognition import ChessRecognizer
import socket
import json
import chess
# Define the server address and port
SERVER_ADDRESS = '192.168.1.101'
SERVER_PORT = 5555


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)
while True:

    # Wait for a client to connect
    print('Waiting for a client to connect...')
    client_socket, client_address = server_socket.accept()
    print(f'Client connected: {client_address}')
    response = None

    while True:
        # Receive a message from the client
        try:
            data = client_socket.recv(1024).decode()
        except ConnectionResetError:
            break

        if not data:
            # If the client has closed the connection, break out of the loop
            break

        # Parse the message as JSON
        try:
            board = ''
            message = json.loads(data)
            img_data = message['img_data']
            img_data = json.loads(img_data)
            turn = message['turn']
            print(f'Received message: {img_data}')
            if turn:
                board, corners = ChessRecognizer.predict(img_data, chess.WHITE)

            if not turn:
                board, corners = ChessRecognizer.predict(img_data, chess.BLACK)
            response = board.board_fen()

        except Exception as e:
            print(f'Error parsing JSON: {e}')
    # Close the client connection
    response_json = json.dumps(response)
    client_socket.close()
    print(f'Client disconnected: {client_address}')

# Close the server socket
server_socket.close()
