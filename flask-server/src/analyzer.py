import chess
from stockfish import Stockfish

class ChessAnalyzer:
  def __init__(self, path, depth= 16, skill_level = 16):
    self.MISTAKE_THRESHOLD = 100
    self.BLUNDER_THRESHOLD = 150
    self.MATE_VALUE = 10000
    self.engine = Stockfish(path)
    self.engine.set_depth(depth)
    self.engine.set_skill_level(skill_level)

  
  def get_relative_score(self, fen, player_color):
    self.engine.set_fen_position(fen)
    eval = self.engine.get_evaluation()

    # centipions pour les évaluations normales, mate pour les mats
    if eval['type'] == 'cp':
      score = eval['value']
    else:
    # On garde le signe de Stockfish (positif si Blanc gagne, négatif si Noir gagne)
      signe = 1 if eval['value'] > 0 else -1
      score = signe * (self.MATE_VALUE - abs(eval['value']))

    # Ajuster le score relativement à la couleur du joueur
    if player_color == chess.BLACK:
      score *= -1
    
    return score

  def error_type(self, prev_score, current_score):
    diff = prev_score - current_score
    if diff >= self.BLUNDER_THRESHOLD:
      return 'Blunder'
    elif diff >= self.MISTAKE_THRESHOLD:
      return 'Mistake'
    return None

  def error_found (self, diff):
    return True if diff >= self.MISTAKE_THRESHOLD else False


    
