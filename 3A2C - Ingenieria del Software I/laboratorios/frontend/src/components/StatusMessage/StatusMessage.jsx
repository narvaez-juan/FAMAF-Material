export default function StatusMessage({ message, color = "white" }) {
  const colorMap = {
    red: "text-red-500",
    yellow: "text-yellow-400",
    white: "text-white",
  };

  const colorClass = colorMap[color] || "text-white";

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <p className={`text-3xl font-semibold text-center ${colorClass}`}>
        {message}
      </p>
    </div>
  );
}