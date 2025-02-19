import { Game } from "../_lib/types";

type Props = {
  game: Game;
};
export default function Board({ game }: Props) {
  const { isComplete, gameBoard } = game;
  return (
    <>
      <div> is game complete? {isComplete ? "True" : "False"} </div>
      <div> {JSON.stringify(gameBoard)} </div>
    </>
  );
}
