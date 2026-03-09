import OponentSecrets from "../OponentSecrets/OponentSecrets";
import OponentSets from "../OponentSets/OponentSets";

export default function PlayerInfo({ jugador, esTurnoActual, playerId }) {
  return (
    <div
      className={`rounded-lg p-2 text-left font-metamorphous ${
        esTurnoActual
          ? "bg-gradient-to-br from-yellow-600 via-yellow-700 to-yellow-800 border-2 border-yellow-300 shadow-[0_0_4px_#c2a22d]"
          : "bg-slate-900 border border-slate-700 shadow-[0_0_4px_#c2a22d]"
      }`}
    >
      <p className="font-bold text-base mb-1 text-white font-metamorphous">
        {jugador.nombre.length > 20
          ? jugador.nombre.slice(0, 17) + "..."
          : jugador.nombre}
      </p>
      <OponentSecrets jugador={jugador} playerId={playerId} />
      <OponentSets jugador={jugador} playerId={playerId} />
    </div>
  );
}
