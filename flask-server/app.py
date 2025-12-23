from flask import Flask, request, jsonify
from flask_cors import CORS
from io import StringIO
from dotenv import load_dotenv
import chess
import chess.pgn
import os
import tqdm
from src.analyzer import ChessAnalyzer
from src.coach import AICoach


load_dotenv()

app = Flask(__name__)
CORS(app)

analyzer = ChessAnalyzer(os.getenv('STOCKFISH_PATH'))
ai_coach = AICoach(os.getenv('API_KEY'))

@app.route('/analyze', methods=['POST'])
def analyze_game():
      pgn_data = request.get_json().get('pgn')
      if not pgn_data:
        return jsonify({'error': 'PGN data not found in request'}), 400
    
        # Transform json into readable chess data
      pgn_io = StringIO(pgn_data)
      game = chess.pgn.read_game(pgn_io)
      board = chess.Board()
      errors = {}

      for move in tqdm.tqdm(game.mainline_moves()):
        player_color = board.turn 
        old_fen = board.fen()
    
        score_before = analyzer.get_relative_score(old_fen, player_color)
    
        board.push(move)
        new_fen = board.fen()
    
        score_after = analyzer.get_relative_score(new_fen, player_color)
    
        diff = score_before - score_after
        if analyzer.error_found(diff):
          errors[move.uci()] = {
          'error_type' : analyzer.error_type(score_before, score_after),
          'board_after_move' : new_fen, 
          'board_before_move' : old_fen,
          'color' : "White" if board.turn == chess.BLACK else "Black"
          }
      
      ai_descriptions = {}
      for move, desc in errors.items():
        explanation = ai_coach.get_explanation(
          fen=desc['board_after_move'],
          move=move,
          eval_diff=score_before - score_after,
          color=desc['color']
        )
        ai_descriptions[move] = explanation

      return jsonify({'message': 'PGN data received and processed successfully', 'errors': errors,'ai_descriptions': ai_descriptions}), 200

if __name__ == '__main__':
    app.run(debug=True)        
        




