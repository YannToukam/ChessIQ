from io import StringIO
import chess
import chess.pgn
import tqdm
from flask import Flask, request, jsonify
from flask_cors import CORS
from stockfish import Stockfish

app = Flask(__name__)
CORS(app)

# Initialize Stockfish engine and thresholds
stockfish_path = r"C:\Users\yanny\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
stockfish = Stockfish(stockfish_path)
stockfish.set_depth(16)
stockfish.set_skill_level(16)

MISTAKE_THRESHOLD = 100
BLUNDER_THRESHOLD = 150

type_errors = {}



@app.route('/analyze', methods=['POST'])
def analyze_pgn():
    try:
        # Receive and log incoming PGN data
        pgn_data = request.json.get('pgn')
        if not pgn_data:
            return jsonify({'error': 'PGN data not found in request'}), 400

        print(pgn_data)

        pgn_io = StringIO(pgn_data)
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            return jsonify({'error': 'Invalid PGN data'}), 400

        # Process moves
        board = chess.Board()
        move_cp_value = []
        

        def error_classifier(cp1, cp2, player_move, board_fen):
            error_type = None
            
            if MISTAKE_THRESHOLD <= (cp1 - cp2) < BLUNDER_THRESHOLD:
                error_type = 'Mistake'
            elif (cp1 - cp2) >= BLUNDER_THRESHOLD:
                error_type = 'Blunder'

            if error_type:
                type_errors[player_move] = {'error_type': error_type, 'board_fen': board_fen}

        for i, move in enumerate(tqdm.tqdm(game.mainline_moves())):
            board.push(move)

            if i % 2 == 0:
                stockfish.set_fen_position(board.fen())
                move_evaluation = stockfish.get_evaluation()['value']
                move_cp_value.append(move_evaluation)
                eval_index = i // 2
                if 0 < eval_index < len(move_cp_value):
                    error_classifier(move_cp_value[eval_index - 1], move_cp_value[eval_index], move.uci(), previous_board)
            previous_board = board.fen()

        print(f"Error moves from the player: {type_errors}")
        # print(move_cp_value)

        return jsonify({'message': 'PGN data received and processed successfully', 'errors': type_errors})

    except KeyError:
        return jsonify({'error': 'PGN data not found in request'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gameAnalysis', methods=['GET'])
def get_computer_moves():
    for desc in type_errors.values():
        stockfish.set_fen_position(desc['board_fen'])
        best_move = stockfish.get_best_move()
        print(best_move +"\n")
        return jsonify({'best_move': best_move})

if __name__ == '__main__':
    app.run(debug=True)