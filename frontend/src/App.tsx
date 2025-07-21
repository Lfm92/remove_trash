import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

type Cell = {
  trash: boolean;
  base: boolean;
  //robot: boolean;
};

type Robot = {
  x: number;
  y: number;
  carrying: boolean;
};

const GRID_SIZE = 32;

function App() {
  const [grid, setGrid] = useState<Cell[][]>([]);
  const [robots, setRobots] = useState<Robot[]>([]);
  const [turn, setTurn] = useState(0);
  const [loading, setLoading] = useState(false);
  const [trashCollected, setTrashCollected] = useState(0);
  const [remainingTrash, setRemainingTrash] = useState(0);

  const fetchState = async () => {
    const res = await axios.get("http://localhost:8000/api/state/");
    setGrid(res.data.grid);
    setTurn(res.data.turn);
    setTrashCollected(res.data.base);
    setRobots(res.data.robots);
    setRemainingTrash(res.data.remaining_trash);
  };

  const stepSimulation = async () => {
    try {
      setLoading(true);
      await axios.post("http://localhost:8000/api/step/");
      await fetchState();
    } catch (error) {
      console.error("Error stepping simulation:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchState();
  }, []);

  const isRobotAt = (x: number, y: number) => {
    return robots.some((r) => r.x === x && r.y === y);
  };

  return (
    <div className="app">
      <h1>WALL-E Simulation</h1>
      <p>Turn: {turn}</p>
      <button onClick={stepSimulation} disabled={loading}>
        {loading ? "Processing..." : "Next Step"}
      </button>
      <p>Trash collected: {trashCollected}</p>
      <p>Trash remaining: {remainingTrash}</p>

      <div className="grid">
        {grid.map((row, y) => (
          <div key={y} className="row">
            {row.map((cell, x) => {
              let className = "cell";
              if (cell.base) className += " base";
              else if (isRobotAt(x, y)) className += " robot";
              else if (cell.trash) className += " trash";
              return <div key={x} className={className} />;
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
