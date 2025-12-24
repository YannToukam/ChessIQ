from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
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
    
      errors, score_before, score_after = analyzer.find_all_errors(pgn_data)
      
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
        




