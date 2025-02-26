"use client";

import clsx from "clsx";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { Game } from "../_lib/types";
import Cell from "./Cell";
import { updateGame } from "../_lib/games.service";
import ReturnHomeButton from "../../_components/ReturnHomeButton";

type Props = {
  game: Game;
};

export default function Board({ game }: Props) {
  const [gameState, setGameState] = useState<Game>(game);
  const mutation = useMutation({
    mutationFn: updateGame,
    onSuccess: (game: Game) => {
      setGameState(game);
    }
  });
  const onClick = (index: number) => {
    mutation.mutate({
      game_id: game.id,
      cell_index: index,
    })
  };
  const { isComplete, gameBoard } = gameState;
  const numberOfColumns = Math.floor(Math.sqrt(gameBoard.length));
  const numberOfCellsCleared = gameBoard.filter(
    (cell) => cell != null && cell > -1
  ).length;
  const isGameOver = isComplete && gameBoard.some((cell) => cell != null && cell === -1);

  return (
    <div className="flex flex-col gap-4 justify-center items-center h-screen">
      {isComplete && <div className="text-2xl ">{isGameOver ? 'GAME OVER' : 'CLEARED!'}</div>}
         <div className="font-semibold text-xl">
        Number of Cells Cleared: {numberOfCellsCleared}
      </div>
       <div className="flex justify-center items-center">
        <div className={clsx("grid gap-2", `grid-cols-${numberOfColumns}`)}>
          {gameBoard.map((value, index) => (
            <Cell
              key={`cell-${index}`}
              value={value}
              index={index}
              handleClick={onClick}
              isDisabled={isComplete}
            />
          ))}
        </div>
      </div>
      {isComplete && <ReturnHomeButton />}
    </div>
  );
}
