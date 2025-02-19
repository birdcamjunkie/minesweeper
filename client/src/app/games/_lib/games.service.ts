export async function getNewGame(): Promise<Game> {
  // TODO: actually POST to /games to get new game
  return Promise.resolve({
    id: "MTE",
    isComplete: false,
    gameBoard: [null, null, null, null, null, null, null, null, null],
  });
}

export async function getGame(game_id: string): Promise<Game> {
  // GET to /games/[:id] to get a game
  // return existing game object
  if (game_id === "MTE") {
    return Promise.resolve({
      id: "MTE",
      isComplete: false,
      gameBoard: [null, null, null, null, null, null, null, null, null],
    });
  }
  return null;
}

export async function updateGame(
  game_id: string,
  cell_index: number
): Promise<Game> {
  // PUT to /games/[:id]/cell[:cell_index] to update game
  // return the updated game object
}
