from io import StringIO
import chess
import chess.pgn
import tqdm
from flask import Flask, request, jsonify
from flask_cors import CORS
from stockfish import Stockfish
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Stockfish engine and thresholds
stockfish_path = os.getenv('STOCKFISH_PATH')
if not stockfish_path or not os.path.isfile(stockfish_path):
    raise ValueError("Invalid or missing STOCKFISH_PATH environment variable")

stockfish = Stockfish(stockfish_path)
stockfish.set_depth(16)
stockfish.set_skill_level(16)

MISTAKE_THRESHOLD = 100
BLUNDER_THRESHOLD = 150


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
        type_errors = {}

        def error_classifier(cp1, cp2, player_move, prev_board_fen, current_board_fen):
            error_type = None

            if MISTAKE_THRESHOLD <= (cp1 - cp2) < BLUNDER_THRESHOLD:
                error_type = 'Mistake'
            elif (cp1 - cp2) >= BLUNDER_THRESHOLD:
                error_type = 'Blunder'
                
            if error_type:
                type_errors[player_move] = {'error_type': error_type, 'board_fen': prev_board_fen,
                                            'eval_diff': cp1 - cp2, 'current_board_fen': current_board_fen}

        previous_board = ""
        for i, move in enumerate(tqdm.tqdm(game.mainline_moves())):
            board.push(move)

            if i % 2 == 0:
                stockfish.set_fen_position(board.fen())
                move_evaluation = stockfish.get_evaluation()['value']
                move_cp_value.append(move_evaluation)
                eval_index = i // 2
                p_move = move.uci()[0:2] + '-' + move.uci()[2:]
        
                if 0 < eval_index < len(move_cp_value):
                    error_classifier(move_cp_value[eval_index - 1], move_cp_value[eval_index], p_move, previous_board,
                                     board.fen())
            previous_board = board.fen()

        print()
        print("-----------------------------------------------")

        print(f"Error moves from the player: {type_errors}")

        ai_descriptions = {}
        for move, desc in type_errors.items():
            try:
                ai_explanation = ai_description(move, desc["current_board_fen"], desc["eval_diff"])
                ai_descriptions[move] = ai_explanation
                type_errors[move]['ai_description'] = ai_explanation
            except Exception as e:
                print(f"Error generating AI description for move {move}: {str(e)}")

        print(ai_descriptions)

        return jsonify({'message': 'PGN data received and processed successfully', 'errors': type_errors,
                        'ai_descriptions': ai_descriptions})

    except KeyError:
        return jsonify({'error': 'PGN data not found in request'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def ai_description(player_error, fen, eval_diff):
    # Fetch the API key from the environment
    api_key = os.getenv('API_KEY')

    if not api_key:
        raise ValueError("API key is missing or invalid")

    print(f"Using API Key: {api_key}")

    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Analyze the chess position described by this FEN: {fen}. It was white's turn and the move {player_error} was played. Stockfish gives an evaluation difference of {eval_diff} after the white player move. This move doesn't violate chess rules, but explain in simple terms why it is a wrong move for this position. Focus strictly on the given FEN and the move. Do not assume additional threats or create hypothetical scenarios beyond what the position shows. Keep the explanation concise and relevant to the FEN."

            }],
            model="llama-3.3-70b-versatile",
            max_tokens=200
        )

        # Return the AI-generated explanation
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error generating AI description: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)