import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingPage from "./LoadingPage";


function LoadGame() {
  const [pgnData, setPgnData] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const navigate = useNavigate();

  async function sendPGN(pgnData) {
    const url = 'http://localhost:5000/analyze';
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pgn: pgnData })
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const responseData = await response.json();
      setIsAnalyzing(false); // Hide loading page
      navigate('/gameAnalysis', { state: { responseData } }); // Navigate to GameAnalysis with state
    } catch (error) {
      console.error('Error:', error);
      setIsAnalyzing(false); // Hide loading page on error
    }
  }

  function handleLoadGameClick() {
    setIsAnalyzing(true); // Show loading page
    sendPGN(pgnData);
  }

  function handleInputChange(event) {
    setPgnData(event.target.value);
  }

  return (
    <div className="input-container">
      {isAnalyzing ? (
        <LoadingPage />
      ) : (
        <>
          <textarea
            name="pgnArea"
            id="pgn-area"
            value={pgnData}
            onChange={handleInputChange}
            placeholder="Paste your PGN file here"
          />
          <button
            id="load-game"
            type="button"
            onClick={handleLoadGameClick}
            disabled={!pgnData.trim()}
          >
            Load Game
          </button>
        </>
      )}
    </div>
  );
}

export default LoadGame;

