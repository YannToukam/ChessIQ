# ♟️ ChessIQ

An intelligent chess application combining React and Flask with Stockfish engine integration.

## 🎯 About

ChessIQ is a modern chess application featuring:
- Interactive chess interface built with React
- Flask backend for game logic and analysis
- Stockfish chess engine integration for powerful move analysis
- Clean separation between frontend and backend for easy deployment

## 🛠️ Tech Stack

**Frontend:** React, React Router DOM  
**Backend:** Flask, Flask-CORS  
**Chess Engine:** Stockfish

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
npm install
```

### Step 4: Setup Backend
```bash
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

**Your Name**  
GitHub: [@your-username](https://github.com/your-username)

---

⭐ Star this repo if you like it!
