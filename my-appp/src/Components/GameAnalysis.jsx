import React, { useState, useEffect} from "react";
import { useLocation } from "react-router-dom";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";


function GameAnalysis() {
  const location = useLocation();
  const { responseData } = location.state || {}; 

  const [currentIndex, setCurrentIndex] = useState(0);
  

  const errors = Object.keys(responseData.errors);
  const currentError = responseData.errors[errors[currentIndex]];
  const [game, setGame] = useState(new Chess(currentError.board_before_move));

  const description = Object.keys(responseData.ai_descriptions)
  const currentDescription = responseData.ai_descriptions[description[currentIndex]]
  console.log(currentDescription)


  useEffect(() => {
    if (currentError.board_before_move) {
      setGame(new Chess(currentError.board_before_move));
    }
  }, [currentError]);


  if (!responseData || !responseData.errors) {
    return <div>Error: Invalid response data</div>;
  }

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % errors.length);
  };

  function makeAMove(move){

    try {
    const gameCopy = new Chess(game.fen());
    
    const result = gameCopy.move(move); 

  if (result) {
    setGame(gameCopy); 
  }
    
    return result
    } catch(error){
      console.log()
    }
  }
  

  function onDrop(sourceSquare, targetSquare){
    const moveData = {
      from: sourceSquare,
      to: targetSquare,
      //promotion: "q",
    };
    const move = makeAMove(moveData);

    // illegal move
    if (move === null) return false;

    return true;
    
  }

  return (
    <div className="puzzle-container">
      <div className="sidebar">
        {currentError && (
          <div className="error-details">
            <div className="error-item">
              <strong>Move :</strong> {errors[currentIndex]}<br />
              <br />
              <strong>Error Type :</strong> {currentError.error_type}<br />
              <br />
              
              <strong>Description : </strong>{currentDescription}

            </div>
          </div>
        )}
        <button className="button-next" onClick={handleNext}>Next</button>
      </div>
      <div className="chessboard-container">
        {currentError && (
          <Chessboard 
            boardWidth={600} 
            position={game.fen()} onPieceDrop={onDrop} 
          />
        )}
      </div>
    </div>
  );
}


export default GameAnalysis;
