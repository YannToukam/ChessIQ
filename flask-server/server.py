from flask import Flask, request, jsonify
from flask_cors import CORS
from stockfish import Stockfish
import chess
import chess.pgn
import tqdm

app = Flask(__name__)
CORS(app) 

# Initialize Stockfish engine
stockfish_path = r"C:\Users\yanny\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
stockfish = Stockfish(stockfish_path)
stockfish.set_depth(16)
stockfish.set_skill_level(16)

# Inaccuracy between 30 to <50 in stockfish eval change
INACCURACY_THRESHOLD = 30

# Mistake between 50> to <150 in stockfish eval change
MISTAKE_THRESHOLD = 50

# Blunder more than 150> cp in stockfish eval change
BLUNDER_THRESHOLD = 150

#METTRE LA GAME SOUS FICHIER CSV

@app.route('/analyze', methods=['POST'])
def analyze_pgn():
    try:
        pgn_data = request.json['pgn']
        print(f"Received PGN data: {pgn_data}")

        # Load the PGN
        game = chess.pgn.read_game(chess.StringIO(pgn_data))

        # Process moves
        board = game.board()
        move_cp_value = []
        type_errors = {}

        def error_classifier(cp1, cp2, player_move):
            if INACCURACY_THRESHOLD <= (cp1 - cp2) < MISTAKE_THRESHOLD:
                type_errors[player_move] = 'inaccuracy'
            elif MISTAKE_THRESHOLD <= (cp1 - cp2) < BLUNDER_THRESHOLD:
                type_errors[player_move] = 'mistake'
            elif (cp1 - cp2) >= BLUNDER_THRESHOLD:
                type_errors[player_move] = 'blunder'

        for i, move in tqdm.tqdm(enumerate(game.mainline_moves())):
            board.push(move)

            if i % 2 == 0:  # It's white's move
                stockfish.set_fen_position(board.fen())
                move_evaluation = stockfish.get_evaluation()['value']
                move_cp_value.append(move_evaluation)
                eval_index = i // 2
                if 0 < eval_index < len(move_cp_value):
                    error_classifier(move_cp_value[eval_index - 1], move_cp_value[eval_index], move.uci())

        print(type_errors)
        print(move_cp_value)

        return jsonify({'message': 'PGN data received and processed successfully'})
    
    except KeyError:
        return jsonify({'error': 'PGN data not found in request'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
