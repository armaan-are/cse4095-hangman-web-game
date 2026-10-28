(function () {
  "use strict";

  const elements = {
    body: document.body,
    difficulty: document.querySelector("#difficulty"),
    newGame: document.querySelector("#new-game"),
    message: document.querySelector("#message-text"),
    error: document.querySelector("#error-message"),
    pattern: document.querySelector("#word-pattern"),
    finalWord: document.querySelector("#final-word"),
    guessedLetters: document.querySelector("#guessed-letters"),
    incorrectLetters: document.querySelector("#incorrect-letters"),
    attempts: document.querySelector("#attempts-text"),
    statusBadge: document.querySelector("#game-status-badge"),
    incorrectCount: document.querySelector("#incorrect-count"),
    progressFill: document.querySelector("#progress-fill"),
    keyboard: document.querySelector("#keyboard"),
    letterButtons: Array.from(document.querySelectorAll("[data-letter]")),
    figureParts: Array.from(document.querySelectorAll(".figure-part")),
  };

  let activeGameId = null;
  let currentState = null;
  let requestVersion = 0;
  let requestPending = false;

  async function requestJson(url, options = {}) {
    const response = await fetch(url, {
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      },
    });

    let payload = null;
    try {
      payload = await response.json();
    } catch (error) {
      throw new Error("The server returned an unreadable response.");
    }

    if (!response.ok) {
      throw new Error(payload.error || `Request failed with status ${response.status}.`);
    }
    return payload;
  }

  function setError(message = "") {
    elements.error.textContent = message;
    elements.error.hidden = !message;
  }

  function formatLetters(letters) {
    return letters.length ? letters.join(" · ").toUpperCase() : "None yet";
  }

  function gameMessage(state) {
    if (!state) {
      return "Choose a difficulty and start a new game.";
    }
    if (state.status === "won") {
      return "You found it! Start a new game whenever you are ready.";
    }
    if (state.status === "lost") {
      return "That was the sixth miss. Try another word when you are ready.";
    }
    if (state.incorrect_letters.length === 0) {
      return "The round is live. Choose your first letter.";
    }
    return "Keep going—the server has updated the puzzle.";
  }

  function render() {
    const state = currentState;
    const status = state ? state.status : "not-started";
    const guessed = state ? state.guessed_letters : [];
    const incorrect = state ? state.incorrect_letters : [];
    const remaining = state ? state.remaining_guesses : 6;
    const incorrectTotal = 6 - remaining;
    const canGuess = Boolean(state && status === "playing" && !requestPending);

    elements.body.dataset.gameState = status;
    elements.message.textContent = gameMessage(state);
    elements.pattern.textContent = state ? state.pattern : "—";
    elements.pattern.setAttribute(
      "aria-label",
      state ? `Word pattern: ${state.pattern}` : "No active word"
    );
    elements.guessedLetters.textContent = formatLetters(guessed);
    elements.incorrectLetters.textContent = formatLetters(incorrect);
    elements.attempts.textContent = `${remaining} ${remaining === 1 ? "attempt" : "attempts"} remaining`;
    elements.statusBadge.textContent =
      status === "not-started" ? "Ready" : status === "playing" ? "Playing" : status;
    elements.incorrectCount.textContent = String(incorrectTotal);
    elements.progressFill.style.width = `${(incorrectTotal / 6) * 100}%`;

    elements.figureParts.forEach((part, index) => {
      part.classList.toggle("is-visible", index < incorrectTotal);
    });

    if (state && state.word && status !== "playing") {
      elements.finalWord.textContent = `The word was “${state.word.toUpperCase()}”.`;
      elements.finalWord.hidden = false;
    } else {
      elements.finalWord.textContent = "";
      elements.finalWord.hidden = true;
    }

    elements.letterButtons.forEach((button) => {
      const letter = button.dataset.letter;
      const wasGuessed = guessed.includes(letter);
      button.disabled = !canGuess || wasGuessed;
      button.classList.toggle("is-guessed", wasGuessed);
      button.setAttribute("aria-pressed", wasGuessed ? "true" : "false");
    });

    elements.difficulty.disabled = requestPending;
    elements.newGame.disabled = requestPending;
    elements.newGame.textContent = requestPending ? "Working…" : "New game";
  }

  async function startGame() {
    const version = ++requestVersion;
    requestPending = true;
    setError();
    render();

    try {
      const state = await requestJson("/api/games", {
        method: "POST",
        body: JSON.stringify({ difficulty: elements.difficulty.value }),
      });
      if (version !== requestVersion) {
        return;
      }
      activeGameId = state.game_id;
      currentState = state;
    } catch (error) {
      if (version === requestVersion) {
        setError(`Could not start a game: ${error.message}`);
      }
    } finally {
      if (version === requestVersion) {
        requestPending = false;
        render();
      }
    }
  }

  async function submitGuess(letter) {
    if (
      requestPending ||
      !activeGameId ||
      !currentState ||
      currentState.status !== "playing" ||
      currentState.guessed_letters.includes(letter)
    ) {
      return;
    }

    const gameId = activeGameId;
    const version = ++requestVersion;
    requestPending = true;
    setError();
    render();

    try {
      const state = await requestJson(`/api/games/${gameId}/guess`, {
        method: "POST",
        body: JSON.stringify({ letter }),
      });
      if (version !== requestVersion || gameId !== activeGameId) {
        return;
      }
      currentState = state;
    } catch (error) {
      if (version === requestVersion && gameId === activeGameId) {
        setError(`That guess was not accepted: ${error.message}`);
      }
    } finally {
      if (version === requestVersion) {
        requestPending = false;
        render();
      }
    }
  }

  elements.newGame.addEventListener("click", startGame);

  elements.keyboard.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-letter]");
    if (button) {
      submitGuess(button.dataset.letter);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey || event.repeat) {
      return;
    }
    if (["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement.tagName)) {
      return;
    }
    const letter = event.key.toLowerCase();
    if (/^[a-z]$/.test(letter)) {
      event.preventDefault();
      submitGuess(letter);
    }
  });

  render();
})();
