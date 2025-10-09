import React from 'react';
import {Link } from "react-router-dom";


const Header = () => {
  return (
    <header className="header">
      <Link className="logo" to= "/">ChessIQ</Link>
      <nav className="nav">
        <Link to= "gameAnalysis">Game Analysis</Link>
        <Link to="puzzles">Puzzles</Link>
      </nav>
      
    </header>
  );
}

export default Header;
