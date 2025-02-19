import Board from "../_components/Board";
import { getGame } from "../_lib/games.service";
import { notFound } from "next/navigation";

export default async function GamePage(params) {
  const game = await getGame("MTE");
  if (!game) {
    return notFound();
  }

  return (
    <>
      <div>Status: {game.isComplete} </div>
      <Board game={game} />
    </>
  );
}
