import './App.css';
import Header from './Components/Header';
import LoadGame from './Components/LoadGame';
import GameAnalysis from './Components/GameAnalysis';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Puzzles from './Components/Puzzles';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<LoadGame />} />
          <Route path="/gameAnalysis" element={<GameAnalysis />} />
          <Route path="/puzzles" element={<Puzzles />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

