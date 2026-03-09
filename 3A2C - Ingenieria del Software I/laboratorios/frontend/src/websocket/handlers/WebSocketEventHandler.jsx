import { offTheTableHandler } from "./CardsOfTheTable/CardsOfTheTableHandler";
import { deadCardFollyHandler } from "./DeadCardFolly/DeadCardFollyHandler";
import { earlyTrainHandler } from "./EarlyTrainToPaddington/EarlyTrainToPaddingtonHandler";
import { delayMurderEscapedHandler } from "./DelayMurderEscaped/DelayMurderEscapedHandler";
import { lookIntoTheAshesHandler } from "./LookIntoTheAshesHandler/LookIntoTheAshesHandler";
import { anotherVictimHandler } from "./AnotherVictim/AnotherVictimHandler";
import { PointYourSuspicionsHandler } from "./PointYourSupcicions/PointYourSuspicionsHandler";

export function handleGameEvent(payload, playerId, players) {
  if (!payload) return;

  switch (payload.card_name) {
    case "Cards Off The Table":
      offTheTableHandler(payload, playerId, players);
      break;
    case "Dead Card Folly":
      deadCardFollyHandler(payload, playerId, players);
      break;
    case "Delay the Murderer’s Escape!":
      delayMurderEscapedHandler(payload, playerId, players);
      break;
    case "Early Train to Paddington":
      earlyTrainHandler(payload, playerId, players);
      break;
    case "Look into the Ashes":
      lookIntoTheAshesHandler(payload, playerId, players);
      break;
    case "Another Victim":
      anotherVictimHandler(payload, playerId, players);
      break;
    case "Point Your Suspicion":
      PointYourSuspicionsHandler(payload, playerId, players);
      break;
    default:
      console.warn("Unhandled event:", payload);
  }
}
