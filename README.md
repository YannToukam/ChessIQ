# ♟️ ChessIQ

ChessIQ is an intelligent chess analysis platform that combines classical chess engines with Large Language Models (LLMs) to provide strategic evaluations and human-like explanations of moves. It bridges the gap between engine precision and human understanding, helping players learn and improve through natural, conversational insights.

## 🎯 About

- 💡 **ChessIQ** is an AI-powered chess analysis platform built to make learning and improvement more **interactive** and **explainable**.  
- ⚙️ Combines the analytical precision of **Stockfish** with the contextual reasoning of **Large Language Models (LLMs)**.  
- 🧠 Provides **human-like explanations** of moves, helping players understand not just *what* to play, but *why*.  
- ♟️ Allows users to **load their own games**, visualize variations, and explore alternative strategies directly on the board.  
- 🧩 Designed for players who want both **tactical accuracy** and **strategic understanding** in their analysis.  
- 💬 Demonstrates how **AI explainability** can bridge the gap between **engine evaluation** and **human intuition**.  
- 🎨 Built with a modern **React.js** interface focused on simplicity, clarity, and educational value.


## 🛠️ Tech Stack

**Frontend**
- ⚛️ React.js (JSX Components)
- 🎨 CSS Modules for modular styling

**Backend**
- 🐍 **Flask (Python)** — lightweight backend API for handling analysis requests
- 🔗 **Flask-CORS** — enables secure communication between frontend and backend
- 📡 **REST API** — serves evaluation and LLM-generated explanations
- 🧠 **Integration with Stockfish and LLM endpoints** for hybrid reasoning

## 🚀 Installation

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Stockfish ([Download here](https://stockfishchess.org/download/))

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/ChessIQ.git
cd ChessIQ
```

### Step 2: Install Stockfish
Download Stockfish from the link above and note the path to the executable.

### Step 3: Setup Frontend
```bash
cd my-appp
npm install
```

### Step 4: Setup Backend
```bash
# In another terminal
cd flask-server
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
python -m pip install flask flask-cors python-dotenv
```

### Step 5: Configure Environment
Create a `.env` file in `flask-server/`:
```env
STOCKFISH_PATH=path/to/your/stockfish.exe
```

### Step 6: Run the Application

**Terminal 1 - Backend:**
```bash
cd flask-server
venv\Scripts\activate  # or source venv/bin/activate
python server.py
```

**Terminal 2 - Frontend:**
```bash
npm start
```

Open `http://localhost:3000` in your browser.

## 👨‍💻 Author

**Yann Yvan Toukam Djomo**  
GitHub: [@YannToukam](https://github.com/YannToukam)

---

⭐ Star this repo if you like it!
