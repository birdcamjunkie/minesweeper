"use client";

import clsx from "clsx";

type Props = {
  index: number;
  value: number | null;
  handleClick: (index: number) => void;
};

export default function Cell({ index, handleClick, value }: Props) {
  return (
    <button
      className={clsx(
        "border border-white h-5 w-5 lg:h-10 lg:w-10 flex items-center justify-center text-black text-xl",
        value && "bg-white"
      )}
      onClick={() => handleClick(index)}
    >
      {value != null && `${value}`}
    </button>
  );
}
