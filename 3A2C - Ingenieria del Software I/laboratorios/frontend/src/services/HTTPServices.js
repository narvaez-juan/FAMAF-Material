const createHttpService = () => {
  const baseUrl = import.meta.env.VITE_SERVER_URI || "http://localhost:8000";

  const request = async (endpoint, options = {}) => {
    const url = `${baseUrl}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    console.log("[request] endpoint:", endpoint, "options:", options);

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = new Error("HTTP error");
        error.status = response.status;
        throw error;
      }

      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  };

  const createGame = async (gameData) => {
    return request("/games/create", {
      method: "POST",
      body: JSON.stringify(gameData),
    });
  };

  const getTurnInfo = async (gameId) => {
    return request(`/games/turn/${gameId}`, {
      method: "GET",
    });
  };

  const startGame = async (gameId, playerId) => {
    return request(`/games/${gameId}/start`, {
      method: "POST",
      body: JSON.stringify({ player_id: playerId }),
    });
  };

  const discardCard = async (gameId, playerId, cardsId) => {
    const payload = { card_ids: cardsId.map(Number) };
    return request(`/games/${gameId}/discard/${playerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const drawCard = async (
    game_id,
    player_id,
    draftCardsSelectedIds,
    drawPileSelectedCount
  ) => {
    const payload = {
      player_id,
      draftCardsSelectedIds,
      drawPileSelectedCount,
    };
    console.log("[drawCard] payload:", payload);
    return request(`/games/${game_id}/draw_card`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const joinGame = async (player_name, player_birth_date, game_id) => {
    return request(`/games/${game_id}/join`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        player_name: player_name,
        player_dob: player_birth_date,
      }),
    });
  };

  const finishTurn = async (game_id, player_id) => {
    return request(`/games/${game_id}/turn`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        player_id: player_id,
      }),
    });
  };

  const setPlay = async (game_id, player_id, selectedCards) => {
    return request(`/games/${game_id}/set/${player_id}/play`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        card_ids: selectedCards,
      }),
    });
  };

  const processSet = async (
    game_id,
    { set_id, target_player_id, chosen_secret_id, chosen_set_id }
  ) => {
    return request(`/games/process/set/${game_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        set_id,
        target_player_id,
        chosen_secret_id,
        chosen_set_id,
      }),
    });
  };

  const updateSecret = async (game_id, { player_id, secret_id, effect }) => {
    return request(`/games/update/secret/${game_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player_id, secret_id, effect }),
    });
  };

  const playAriadne = async (
    game_id,
    { AriadneCardId, targetSetId, playerId }
  ) =>
    // ariadneCard, targetSet, RequesterID (reveal secret modal after adding card)
    {
      console.log("Enviando: ", {
        AriadneCardId,
        targetSetId,
        playerId,
      });
      return request(`/games/ariadne_join_set/${game_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ariadne_card_id: AriadneCardId,
          target_set_id: targetSetId,
          player_id: playerId,
        }),
      });
    };

  const stealSecret = async (
    game_id,
    { playerId, targetPlayerId, secretId }
  ) => {
    console.log("Enviando: ", {
      playerId,
      targetPlayerId,
      secretId,
    });
    return request(`/games/steal_secret/${game_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        player_id: playerId,
        target_player_id: targetPlayerId,
        secret_id: secretId,
      }),
    });
  };

  const stealSet = async (game_id, player_id, set_id) => {
    const payload = { set_id };
    console.log("[stealSet] payload:", payload);
    return request(`/games/${game_id}/set/${player_id}/steal`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const cardsOfTheTable = async (gameId, playerId, idCard, targetPlayerId) => {
    const payload = {
      player_id: playerId,
      id_card: idCard,
      target_player_id: targetPlayerId,
    };
    return request(`/games/play/cards-off-table/${gameId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const deadCardFolly = async (gameId, direction, cardsToPass, idCard) => {
    const payload = {
      direction: direction,
      cards_to_pass: cardsToPass,
      id_dead_card_folly: idCard,
    };

    return request(`/games/play/dead-card-folly/${gameId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const earlyTrainToPaddington = async (gameId, playerId, idCard) => {
    const payload = {
      player_id: playerId,
      id_early_train_to_paddington: idCard,
    };

    return request(`/games/play/early-train-to-paddington/${gameId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const murdererEscapes = async (
    gameId,
    playerId,
    discardedCardIds,
    cardId
  ) => {
    const payload = {
      id_delay_the_murderer_escape: cardId,
      player_id: playerId,
      cards_selected: discardedCardIds,
    };

    return request(`/games/play/delay-murderer-escape/${gameId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const lookIntoTheAshes = async (
    gameId,
    playerId,
    eventCardId,
    choosenGameCardId
  ) => {
    const payload = {
      event_card_id: eventCardId,
      chosen_gamecard_id: choosenGameCardId,
    };
    return request(`/games/play/look-into-the-ashes/${gameId}/${playerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const anotherVictim = async (gameId, playerId, setId, cardId) => {
    const payload = {
      set_id: setId,
      event_card_id: cardId,
    };

    return request(`/games/play/another_victim/${gameId}/${playerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  const pointYourSuspicions = async (
    gameId,
    playerId,
    cardId,
    targetPlayersIds
  ) => {
    const payload = {
      player_id: playerId,
      card_id: cardId,
      target_player_ids: targetPlayersIds,
    };
    return request(`/games/play/point-your-suspicion/${gameId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  };

  return {
    createGame,
    getTurnInfo,
    startGame,
    discardCard,
    drawCard,
    drawCard,
    joinGame,
    finishTurn,
    setPlay,
    processSet,
    updateSecret,
    playAriadne,
    stealSecret,
    stealSet,
    cardsOfTheTable,
    deadCardFolly,
    earlyTrainToPaddington,
    murdererEscapes,
    lookIntoTheAshes,
    anotherVictim,
    pointYourSuspicions,
  };
};

export { createHttpService };
