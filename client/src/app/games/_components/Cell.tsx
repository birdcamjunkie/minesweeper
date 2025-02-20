"use client";

import clsx from "clsx";

type Props = {
  index: number;
  value: number | null;
  handleClick: (index: number) => void;
  isDisabled: boolean;
};

export default function Cell({ index, handleClick, value, isDisabled }: Props) {
  return (
    <button
      className={clsx(
        "border border-white h-5 w-5 lg:h-10 lg:w-10 flex items-center justify-center text-black text-lg lg:text-xl",
        value != null && "bg-white"
      )}
      disabled={isDisabled}
      onClick={() => handleClick(index)}
    >
      {value != null && value > 0 ? `${value}` : value === 0 ? "" : "x"}
    </button>
  );
}
