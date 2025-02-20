"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";
import { useMutation } from "@tanstack/react-query";
import { getNewGame } from "../games/_lib/games.service";

export default function StartGameButton() {
  const router = useRouter();
  const mutation = useMutation({
    mutationFn: getNewGame,
    onSuccess: (game: Game) => {
      router.push(`/games/${game.id}`);
    },
    onError: () => {
      // TODO: make a popup on page
      console.log('Failed to create a game')
    }
  });

  const onClickHandler = () => {
    mutation.mutate();
  };

  return (
    <div
      className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
      onClick={onClickHandler}
    >
      <Image
        className="dark:invert"
        src="/vercel.svg"
        alt="Vercel logomark"
        width={20}
        height={20}
      />
      Start a game
    </div>
  );
}
