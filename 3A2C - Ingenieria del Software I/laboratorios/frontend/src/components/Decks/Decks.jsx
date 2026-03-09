import Card from "../Card/Card";
import DiscardPileModal from "../DiscardPile/DiscardPileModal"; // Importa el nuevo componente

export default function Decks({
  drawPileCount = 0,
  drawPilePickCount = 0,
  discardPile = [],
  setDrawPileLeftClicks,
  setDrawPileRightClicks,
  totalSelected = 0,
  discardedCount = 0,
}) {
  const handleMouseClick = (mouse) => {
    if (mouse.button === 0) {
      if (totalSelected >= discardedCount) {
        return;
      }
      setDrawPileLeftClicks((prev) => prev + 1);
    }
    if (mouse.button === 2) {
      setDrawPileRightClicks((prev) => (prev > 0 ? prev - 1 : 0));
    }
  };

  return (
    <div className="flex items-end justify-center gap-12 mt-[-20px] h-52">
      {/* Mazo de robo */}
      <div className="flex flex-col items-center">
        <h3 className="font-semibold text-white font-metamorphous text-sm">
          Draw Pile
        </h3>
        <div
          className="group flex flex-col items-center cursor-pointer transform transition-all duration-300 hover:scale-105"
          onMouseDown={handleMouseClick}
          onContextMenu={(mouse) => mouse.preventDefault()}
        >
          <div className="group relative w-20 h-28 cursor-pointer transform transition-all duration-300 hover:scale-105">
            <div className="absolute top-1 left-1 w-full h-full bg-gray-800 rounded-xl opacity-30 z-0"></div>
            <div className="absolute top-0.5 left-0.5 w-full h-full bg-gray-700 rounded-xl opacity-50 z-0"></div>

            <div className="relative w-20 h-28 rounded-xl shadow-2xl overflow-hidden group-hover:shadow-3xl transition-shadow duration-300">
              <img
                src="/Cartas/01-card_back.png"
                alt="Mazo de cartas"
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110 rounded-xl shadow-2xl relative z-10"
              />
              <div className="absolute bottom-2 z-10 right-2 bg-gradient-to-r from-red-600 to-red-700 text-white text-sm font-bold px-3 py-1.5 rounded-full shadow-lg border-2 border-white">
                {drawPileCount}
              </div>

              {drawPilePickCount > 0 && (
                <div className="absolute top-2 left-2 bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow border-2 border-white z-20">
                  {drawPilePickCount}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Reemplaza el mazo de descarte con el nuevo componente */}
      <DiscardPileModal discardPile={discardPile} />
    </div>
  );
}
