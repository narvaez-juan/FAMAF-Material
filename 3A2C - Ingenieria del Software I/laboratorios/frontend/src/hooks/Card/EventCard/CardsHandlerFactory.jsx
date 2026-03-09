import useCardsOnTheTable from "./CardsOnTheTable/CardsOnTheTableContainer";
import useDeadCardFolly from "./DeadCardFolly/DeadCardFollyContainer";
import useEarlyTrainToPaddington from "./EarlyTrainToPaddington/EarlyTrainToPaddingtonContainer";
import playDelayMurderEscaped from "./DelayMurderEscapes/playDelayMurderEscaped";
import playLookIntoTheAshes from "./LookIntoTheAshes/LookIntoTheAshesContainer";
import playAnotherVictim from "./AnotherVictim/AnotherVictimContainer";
import playPointYourSuspicions from "./PointYourSuspicions/PointYourSuspicionsContainer";

const cardHandlers = {
  "17-event_cardsonthetable.png": useCardsOnTheTable,
  "18-event_anothervictim.png": playAnotherVictim,
  "19-event_deadcardfolly.png": useDeadCardFolly,
  "20-event_lookashes.png": playLookIntoTheAshes,
  "21-event_cardtrade.png": null,
  "22-event_onemore.png": null,
  "23-event_delayescape.png": playDelayMurderEscaped,
  "24-event_earlytrain.png": useEarlyTrainToPaddington,
  "25-event_pointsuspicions.png": playPointYourSuspicions,
};

export const getEventCardHandler = (cardName) => {
  return cardHandlers[cardName] || null;
};
