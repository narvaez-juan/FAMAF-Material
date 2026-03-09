import { describe, it, expect } from "vitest";
import { getEventCardHandler } from "./CardsHandlerFactory";
import useCardsOnTheTable from "./CardsOnTheTable/CardsOnTheTableContainer";
import useDeadCardFolly from "./DeadCardFolly/DeadCardFollyContainer";
import playLookIntoTheAshes from "./LookIntoTheAshes/LookIntoTheAshesContainer";
import playDelayMurderEscaped from "./DelayMurderEscapes/playDelayMurderEscaped";
import useEarlyTrainToPaddington from "./EarlyTrainToPaddington/EarlyTrainToPaddingtonContainer";

describe("getEventCardHandler", () => {
  const cases = [
    ["17-event_cardsonthetable.png", useCardsOnTheTable],
    ["19-event_deadcardfolly.png", useDeadCardFolly],
    ["20-event_lookashes.png", playLookIntoTheAshes],
    ["23-event_delayescape.png", playDelayMurderEscaped],
    ["24-event_earlytrain.png", useEarlyTrainToPaddington],
  ];

  it.each(cases)(
    "devuelve el handler correcto para %s",
    (cardName, expectedHandler) => {
      const handler = getEventCardHandler(cardName);
      expect(handler).toBe(expectedHandler);
    }
  );
});
