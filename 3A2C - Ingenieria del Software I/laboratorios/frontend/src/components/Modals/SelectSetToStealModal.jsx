import Card from "../Card/Card";

export default function SelectSetToStealModal({
  sets,
  playerName,
  loading = false,
  onConfirm,
  onCancel,
}) {
  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div className="bg-gradient-to-b from-blue-900/90 to-slate-900/90 rounded-xl border border-yellow-400/30 shadow-2xl w-full max-w-4xl mx-4">
        {/* Header */}
        <div className="border-b border-yellow-400/30 px-8 py-6">
          <h2 className="text-2xl font-metamorphous font-bold text-yellow-300">
            Steal a Set from {playerName}
          </h2>
          <p className="text-sm text-gray-400 mt-2">
            Select which set you want to steal
          </p>
        </div>

        {/* Content */}
        <div className="p-8 max-h-96 overflow-y-auto">
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-400 font-metamorphous text-lg">
                Loading sets...
              </p>
            </div>
          ) : sets && sets.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {sets.map((set, index) => (
                <button
                  key={set.set_play_id || index}
                  onClick={() => onConfirm(set.set_play_id)}
                  className="group p-6 rounded-lg bg-gradient-to-br from-blue-800/50 to-blue-900/50 
                           border border-yellow-400/20 hover:border-yellow-400/60 hover:shadow-[0_0_12px_rgba(194,162,45,0.4)]
                           transition-all duration-300 text-center"
                >
                  {/* Abanico de cartas */}
                  <div
                    className="flex justify-center items-end mb-4"
                    style={{ height: "140px" }}
                  >
                    <div className="relative flex justify-center items-end">
                      {set.card_game_images &&
                      set.card_game_images.length > 0 ? (
                        set.card_game_images.map((image, cardIndex) => {
                          const total = set.card_game_images.length;
                          const rotation = (cardIndex - (total - 1) / 2) * 5;
                          const translateY =
                            Math.abs(cardIndex - (total - 1) / 2) * 4;
                          const left = cardIndex * 50 - ((total - 1) * 50) / 2;

                          return (
                            <div
                              key={set.card_game_ids[cardIndex]}
                              className="absolute transition-transform duration-300 group-hover:scale-110"
                              style={{
                                transform: `rotate(${rotation}deg) translateY(${translateY}px)`,
                                transformOrigin: "bottom center",
                                left: `${left}px`,
                              }}
                            >
                              <Card
                                image={image}
                                alt="SetCard"
                                size="w-24 h-34"
                              />
                            </div>
                          );
                        })
                      ) : (
                        <div className="text-gray-400">No cards</div>
                      )}
                    </div>
                  </div>

                  {/* Info del set */}
                  <div className="space-y-2">
                    <p className="text-sm text-gray-300 font-metamorphous">
                      Set #{set.set_play_id}
                    </p>
                    <p className="text-lg font-metamorphous font-semibold text-yellow-300 group-hover:text-yellow-200">
                      {set.card_game_images?.length || 0} Cards
                    </p>
                  </div>

                  {/* Indicador de selección */}
                  <div
                    className="mt-4 px-3 py-1 rounded bg-red-600/20 border border-red-500/50 group-hover:border-red-500 
                              group-hover:bg-red-600/40 transition-all"
                  >
                    <span className="text-xs font-metamorphous font-bold text-red-400 group-hover:text-red-300">
                      STEAL
                    </span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-400 font-metamorphous text-lg">
                This player doesn't have any sets to steal
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-yellow-400/30 px-8 py-4 flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 px-4 py-2 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 
                     text-white font-metamorphous font-semibold transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
