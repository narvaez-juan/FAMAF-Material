import { useEffect, useState } from "react";

export default function useCountDown(key, defaultSeconds = 60) {
  // Persist timer
  const saved = parseInt(localStorage.getItem(key), 10);
  const initial = !isNaN(saved) ? saved : defaultSeconds;

  const [secondsLeft, setSecondsLeft] = useState(initial);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    if (!isActive || secondsLeft <= 0) return;

    const timeout = setTimeout(() => {
      setSecondsLeft(secondsLeft - 1);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [secondsLeft, isActive]);

  useEffect(() => {
    localStorage.setItem(key, secondsLeft);
  }, [secondsLeft, key]);

  const start = () => {
    setIsActive(true);
    setSecondsLeft(initial);
  };
  const stop = () => setIsActive(false);
  const reset = (seconds = defaultSeconds) => setSecondsLeft(seconds);

  return { secondsLeft, start, stop, reset };
}
