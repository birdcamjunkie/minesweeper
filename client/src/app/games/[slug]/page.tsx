import Board from "../_components/Board";
import { getGame } from "../_lib/games.service";
import { notFound } from "next/navigation";
import App from "../../_components/App";

type Props = {
  params: Promise<{ slug: string }>;
};

export default async function GamePage({ params }: Props) {
  const slug = (await params).slug;
  const game = await getGame(slug);

  if (!game) {
    return notFound();
  }

  return (
      <Board game={game} />
  );
}
