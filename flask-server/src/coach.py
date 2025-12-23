from groq import Groq

class AICoach:
  def __init__(self, api_key):
    self.client = Groq(api_key=api_key)
  
  def get_explanation(self, fen, move, eval_diff, color):
    prompt = f"Analyze the chess position described by this FEN: {fen}. It was {color}'s turn and the move {move} was played. Stockfish gives an evaluation difference of {eval_diff} after the {color} player move. This move doesn't violate chess rules, but explain in simple terms why it is a wrong move for this position. Focus strictly on the given FEN and the move. Do not assume additional threats or create hypothetical scenarios beyond what the position shows. Keep the explanation concise and relevant to the FEN."

    try :
       response = self.client.chat.completions.create(
          messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama-3.3-70b-versatile",
            max_tokens=200
          
       )
       return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error generating AI description: {e}")
        return None