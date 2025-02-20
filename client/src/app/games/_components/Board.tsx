"use client";

import clsx from "clsx";

import { Game } from "../_lib/types";
import Cell from "./Cell";

type Props = {
  game: Game;
};

export default function Board({ game }: Props) {
  const onClick = (index: number) => console.log(`click on cell ${index}`);
  const { isComplete, gameBoard } = game;
  const numberOfColumns = Math.floor(Math.sqrt(gameBoard.length));
  const numberOfCellsCleared = gameBoard.filter(Boolean).length;

  return (
    <div className="flex flex-col gap-4 justify-center items-center h-screen">
      <div className="font-semibold text-xl">
        Number of cells clicked: {numberOfCellsCleared}
      </div>
      <div className="flex justify-center items-center">
        <div className={clsx("grid gap-2", `grid-cols-${numberOfColumns}`)}>
          {gameBoard.map((value, index) => (
            <Cell
              key={`cell-${index}`}
              value={value}
              index={index}
              handleClick={onClick}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
