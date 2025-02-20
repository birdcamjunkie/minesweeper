import * as changeCaseKeys from "change-case/keys";

export async function getNewGame(): Promise<Game> {
  const response = await fetch("http://localhost:8000/games", {
    method: "POST",
  });
  if (!response.ok) {
    console.log("Failed to generate a new game");
    return null;
  }
  // TODO: handle if response.json() fails
  const data = await response.json();
  return changeCaseKeys.camelCase(data);
}

export async function getGame(game_id: string): Promise<Game> {
  const response = await fetch(`http://localhost:8000/games/${game_id}`);
  if (!response.ok) {
    console.log(`Failed to get game with id ${game_id}`);
    return null;
  }
  const data = await response.json();
  return changeCaseKeys.camelCase(data);
}

export async function updateGame(
  game_id: string,
  cell_index: number
): Promise<Game> {
  const response = await fetch(
    `http://localhost:8000/games/${game_id}/cell${cell_index}`,
    {
      method: "PUT",
    }
  );
  if (!response.ok) {
    console.log("Failed to update the game");
    return null;
  }
  const { data, error } = await response.json();
  return changeCaseKeys.camelCase(data);
}
