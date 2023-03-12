import engine
import socket
import json

engine = engine.engine

# Define the server address and port
SERVER_ADDRESS = '192.168.1.105'
SERVER_PORT = 5556

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
            message = json.loads(data)
            input1 = message['message']
            print(f'Received message: {input1}')
            if input1[0:4] == '-fen':
                engine.set_fen_position(input1[5:])  # sets fen position; example: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
                print('fen->', input1[6:])
                response = {'message': f'game state is set to, {input1[6:]}'}
            elif input1[0:3] == '-bm':
                response = {'message': engine.get_best_move(1000)}  # returns the best move according to stockfish
            elif input1[0:4] == '-gtm':
                response = {'message': engine.get_top_moves()}  # returns top 3 best moves
            elif input1[0:4] == '-ser':
                engine.set_elo_rating(int(input1[5:]))  # sets elo rating range(250-3200)
                response = {'message': f'Elo rating of {input1[5:]} is set'}
            elif input1[0:5] == '-eval':
                response = {'message': engine.get_evaluation()}  # returns evaluation of the current position; examples: {"type":"cp", "value":12}
                                                                                                        # {"type":"mate", "value":-3}
            elif input1[0:4] == '-imc':
                response = {'message': engine.is_move_correct(input1[5:])}  # returns if move is legal; example: input: 'a2a3', output: True
            elif input1[0:5] == '-mfcp':  # makes move from current position; input format: '{move1},{move2},{move3}'; example: "g4d7,a8b8",f1d1"
                moves = input1[6:].split(',')
                response = {'message': engine.make_moves_from_current_position(moves)}
            elif input1[0:4] == '-gws':
                response = {'message': engine.get_what_is_on_square(input1[5:])}  # gets what is on square: example input: 'b3'
            elif input1[0:4] == 'wmc':
                response = {'message': engine.will_move_be_a_capture(input1[5:])}  #Find if a move will be a capture (and if so, what type of capture)
                                                            # examples: input: 'c3d5', output: 1 (direct capture)
                                                            # input: 'e5d6', output: 2 (en passant)
                                                            # input: 'f1e2', output: 0 (no capture)

            response_json = json.dumps(response)

            # Send the response back to the client
            client_socket.send(response_json.encode())
        except Exception as e:
            print(f'Error parsing JSON: {e}')

    # Close the client connection
    client_socket.close()
    print(f'Client disconnected: {client_address}')

# Close the server socket
server_socket.close()

