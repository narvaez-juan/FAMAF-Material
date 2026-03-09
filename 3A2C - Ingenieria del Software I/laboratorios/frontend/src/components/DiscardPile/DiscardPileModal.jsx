import { useEffect, useState } from "react";
import Card from "../Card/Card";
import useDiscardPile from "../../containers/Deck/DiscardPileContainer";
import Button from "../Button/Button";

export default function DiscardPileModal({ discardPile = [] }) {
  const {
    openModalByIntoTheAshes: storeOpenByAshes,
    setOpenModal: storeSetOpenByAshes,
    openDiscardModal: storeOpenDiscardModal,
    setOpenDiscardModal: storeSetOpenDiscardModal,
    setPlayerHasPlayedEvent: storeSetPlayerHasPlayedEvent,
    handleCardClick: containerHandleCardClick,
    setSelectedCards: containerSetSelectedCards,
    selectedCards: containerSelectedCards,
    handleOnConfirm: containerHandleOnConfirm,
    handleOnSelectAshesCard: containerHandleAshes,
  } = useDiscardPile();
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Obtener las últimas 5 cartas
  const lastFiveCards = discardPile.slice(-5);
  const topCard = discardPile.at(-1);

  return (
    <>
      {/* Mazo de descarte */}
      <div className="flex flex-col items-center">
        <h3 className="font-semibold text-white font-metamorphous text-sm">
          Discard Pile
        </h3>
        <div
          className="relative w-20 h-28 cursor-pointer hover:scale-105 transition-transform duration-200"
          onClick={() => setIsModalOpen(true)}
        >
          {topCard ? (
            <Card image={topCard.image} alt="Discarded card" />
          ) : (
            <div className="w-full h-full border-2 border-dashed border-gray-400 rounded-xl flex items-center justify-center bg-gray-800 bg-opacity-30">
              <p className="text-gray-400 text-center text-sm font-metamorphous">
                No cards
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {(isModalOpen || storeOpenDiscardModal || storeOpenByAshes) && (
        <div
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
          onClick={() => setIsModalOpen(false)}
        >
          <div
            className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 max-w-lg w-full mx-4 shadow-2xl border-2 border-gray-700"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white font-metamorphous">
                Last Discarded Cards
              </h2>
            </div>

            {lastFiveCards.length > 0 ? (
              <div className="flex justify-center gap-3 flex-wrap">
                {lastFiveCards.map((card, index) => {
                  const stableKey = card.id;

                  return (
                    <div
                      key={stableKey}
                      className="w-20 h-28 transform hover:scale-110 transition-transform duration-200"
                    >
                      <Card
                        key={stableKey}
                        image={card.image}
                        alt={`Card ${stableKey}`}
                        onClick={() =>
                          containerHandleCardClick(stableKey, card.image)
                        }
                        isSelected={
                          storeOpenDiscardModal || storeOpenByAshes
                            ? containerSelectedCards.some(
                                (card) => card.id === stableKey
                              )
                            : false
                        }
                      />
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-gray-400 text-center py-8 font-metamorphous">
                No discarded cards yet
              </p>
            )}

            <Button
              buttonColor="#8b2e2e"
              buttonHoverColor="#c2322d"
              className="text-white mt-4 w-full"
              onDisabledHandler={false}
              onClickHandler={() => {
                setIsModalOpen(false);
                storeSetOpenDiscardModal(false);
                storeSetPlayerHasPlayedEvent(false);
                storeSetOpenByAshes(false);
                containerSetSelectedCards([]);
              }}
              buttonText="Close"
            />

            {!isModalOpen && storeOpenDiscardModal && (
              <Button
                buttonColor="#0b3b6f"
                buttonHoverColor="#c2a22d"
                className="text-white mt-4 w-full"
                onDisabledHandler={containerSelectedCards.length === 0}
                onClickHandler={() => {
                  storeSetOpenDiscardModal(false);
                  containerHandleOnConfirm();
                }}
                buttonText="Confirm Order"
              />
            )}

            {!isModalOpen && storeOpenByAshes && (
              <Button
                buttonColor="#0b3b6f"
                buttonHoverColor="#c2a22d"
                className="text-white mt-4 w-full"
                onDisabledHandler={containerSelectedCards.length !== 1}
                onClickHandler={() => {
                  storeSetOpenByAshes(false);
                  containerHandleAshes();
                }}
                buttonText="Select Card"
              />
            )}
          </div>
        </div>
      )}
    </>
  );
}
