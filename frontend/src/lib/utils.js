import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export const formatSemesterStatus = (string) => {
  if (string === "open") {
    return "Open";
  } else {
    return "Closed";
  }
};
