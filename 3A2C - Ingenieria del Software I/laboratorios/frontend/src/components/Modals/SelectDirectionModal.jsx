import { useState, useMemo, useEffect } from "react";
import { useDeadCardFollyStore } from "../../Store/DeadCardFollyStore";

export default function SelectDirectionModal() {
  const { setSelectedDirection, setSelectDirection } = useDeadCardFollyStore();
  const [localDirection, setLocalDirection] = useState(null);
  const [secondsLeft, setSecondsLeft] = useState(5);

  const directions = ["left", "right"];

  // Countdown and auto-select random direction after 5s
  useEffect(() => {
    const interval = setInterval(() => {
      setSecondsLeft((prev) => Math.max(prev - 1, 0));
    }, 1000);

    const timer = setTimeout(() => {
      const randomDir =
        directions[Math.floor(Math.random() * directions.length)];
      handleConfirm(randomDir);
    }, 5000);

    return () => {
      clearInterval(interval);
      clearTimeout(timer);
    };
  }, []);

  const handleConfirm = (dir) => {
    if (!dir) return;
    setSelectedDirection(dir);
    setSelectDirection(false);
  };

  const infoText = useMemo(() => {
    return `Select a direction to pass the card. ${secondsLeft} seconds left.`;
  }, [secondsLeft]);

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 flex items-center justify-center">
      <div className="relative bg-gray-900 rounded-2xl shadow-lg p-6 flex flex-col items-center">
        <h2 className="text-white text-xl font-metamorphous mb-4">
          Select Direction
        </h2>

        <p className="text-gray-300 text-center font-metamorphous mb-6 px-6">
          {infoText}
        </p>

        <div className="flex gap-6 mb-6">
          {directions.map((dir) => (
            <button
              key={dir}
              onClick={() => setLocalDirection(dir)}
              className={`px-6 py-2 rounded-xl font-metamorphous font-semibold transition-all
                ${
                  localDirection === dir
                    ? "bg-[#c2a22d] text-black shadow-[0_0_6px_#c2a22d]"
                    : "bg-gray-700 text-gray-400 hover:brightness-90"
                }`}
            >
              {dir.charAt(0).toUpperCase() + dir.slice(1)}
            </button>
          ))}
        </div>

        <button
          onClick={() => handleConfirm(localDirection)}
          disabled={!localDirection}
          className={`inline-flex items-center justify-center rounded-xl px-6 py-2 text-sm font-metamorphous font-semibold shadow-[0_0_6px_#c2a22d] transition-all
            ${
              localDirection
                ? "bg-[#c2a22d] text-black hover:brightness-95"
                : "bg-gray-700 text-gray-400 cursor-not-allowed"
            }`}
        >
          Confirm
        </button>
      </div>
    </div>
  );
}
