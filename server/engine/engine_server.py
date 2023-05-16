import stockfish_launcher
import socket
import json
import traceback

# Create engine object
engine = stockfish_launcher.create_object()

# Define the server address and port
SERVER_ADDRESS = '95.179.202.254'
SERVER_PORT = 5556


def get_fen(input1: str):
    if '-fen' in input1:
        starting_index = input1.index('-fen')
        fen = input1[starting_index + 4:]
        return fen


def set_fen(input1: str, fen):
    if '-fen' in input1:
        engine.set_fen_position(fen)
    elif len(input1) > 10:
        input1 = input1.split(' ')
        fen = input1[1:]
        fen = ' '.join(fen)
        engine.set_fen_position(fen)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
    while True:
        # Wait for a client to connect
        s.listen()
        print('Waiting for a client to connect...')
        conn, addr = s.accept()
        print(f'Client connected: {addr}')
        response = None

        while True:
            # Receive a message from the client
            try:
                data = conn.recv(1024).decode()
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
                try:
                    fen = get_fen(input1)

                    if input1[0:4] == '-fen':
                        engine.set_fen_position(fen)  # sets fen position; example: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
                        print('fen->', fen)
                        response = {'message': f'game state is set to, {input1[6:]}'}
                    elif input1[0:3] == '-bm':
                        set_fen(input1, fen)
                        response = {'message': engine.get_best_move(1000)}  # returns the best move according to stockfish
                    elif input1[0:4] == '-gtm':
                        set_fen(input1, fen)
                        response = {'message': engine.get_top_moves()}  # returns top 3 best moves
                    elif input1[0:4] == '-ser':
                        set_fen(input1, fen)
                        engine.set_elo_rating(int(input1[5:]))  # sets elo rating range(250-3200)
                        response = {'message': f'Elo rating of {input1[5:]} is set'}
                    elif input1[0:5] == '-eval':
                        set_fen(input1, fen)
                        eval = engine.get_evaluation()
                        value = eval['value']
                        #value = round(int(value), 1)
                        eval = f"{eval['type']} {value}"
                        response = {'message': eval}  # returns evaluation of the current position; examples: {"type":"cp", "value":12}
                                                                                                                # {"type":"mate", "value":-3}
                    elif input1[0:4] == '-imc':
                        set_fen(input1, fen)
                        response = {'message': engine.is_move_correct(input1[5:])}  # returns if move is legal; example: input: 'a2a3', output: True
                    elif input1[0:5] == '-mfcp':  # makes move from current position; input format: '{move1},{move2},{move3}'; example: "g4d7,a8b8",f1d1"
                        set_fen(input1, fen)
                        moves = input1[6:].split(',')
                        response = {'message': engine.make_moves_from_current_position(moves)}
                    elif input1[0:4] == '-gws':
                        set_fen(input1, fen)
                        response = {'message': engine.get_what_is_on_square(input1[5:])}  # gets what is on square: example input: 'b3'
                    elif input1[0:4] == 'wmc':
                        set_fen(input1, fen)
                        response = {'message': engine.will_move_be_a_capture(input1[5:])}  #Find if a move will be a capture (and if so, what type of capture)
                                                                    # examples: input: 'c3d5', output: 1 (direct capture)
                                                                    # input: 'e5d6', output: 2 (en passant)
                                                                    # input: 'f1e2', output: 0 (no capture)
                except Exception as e:
                    print(traceback.format_exc())
                    # Reset the engine
                    engine = stockfish_launcher.create_object()
                    response = 'error'

                response_json = json.dumps(response)

                # Send the response back to the client
                conn.send(response_json.encode())
            except Exception as e:
                print(traceback.format_exc())



        # Close the client connection
        conn.close()
        print(f'Client disconnected: {addr}')

    # Close the server socket
    #s.close()

