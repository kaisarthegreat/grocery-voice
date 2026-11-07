(() => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const startButton = document.getElementById("voice-start");
  const stopButton = document.getElementById("voice-stop");
  const languageSelect = document.getElementById("voice-language");
  const status = document.getElementById("voice-status");
  const transcriptView = document.getElementById("voice-transcript");
  const itemInput = document.getElementById("item-input");

  let recognition = null;
  let finalTranscript = "";
  let shouldListen = false;
  let isSubmitting = false;

  function setStatus(message, listening = false) {
    status.textContent = message;
    status.classList.toggle("is-listening", listening);
    startButton.disabled = listening || !SpeechRecognition;
    stopButton.disabled = !listening;
  }

  if (!SpeechRecognition) {
    setStatus("Voice recognition is not supported in this browser.");
    startButton.disabled = true;
    transcriptView.textContent = "You can still type your grocery items in the fields above.";
    return;
  }

  function createRecognition() {
    const instance = new SpeechRecognition();
    instance.lang = languageSelect.value;
    instance.continuous = true;
    instance.interimResults = true;

    instance.onresult = event => {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const phrase = event.results[i][0].transcript.trim();
        if (!phrase) continue;
        if (event.results[i].isFinal) {
          finalTranscript = `${finalTranscript} ${phrase}`.trim();
        } else {
          interim += `${phrase} `;
        }
      }
      const visibleText = `${finalTranscript} ${interim}`.trim();
      transcriptView.textContent = visibleText || "Listening…";
    };

    instance.onerror = event => {
      const messages = {
        "not-allowed": "Microphone permission was denied. Allow microphone access in your browser.",
        "service-not-allowed": "The browser speech service is unavailable.",
        "no-speech": "No speech was detected. Try speaking a little closer to the microphone.",
        "audio-capture": "No microphone was detected. Check your device settings."
      };
      if (event.error !== "no-speech") shouldListen = false;
      setStatus(messages[event.error] || `Speech recognition error: ${event.error}`);
    };

    instance.onend = async () => {
      if (shouldListen) {
        try { instance.start(); return; } catch { shouldListen = false; }
      }
      setStatus("Microphone is off");
      if (!finalTranscript || isSubmitting) return;
      isSubmitting = true;
      try {
        const response = await fetch("/api/voice/transcript", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: finalTranscript, language: languageSelect.value })
        });
        if (!response.ok) throw new Error(`Server returned ${response.status}`);
        const data = await response.json();
        itemInput.value = data.text;
        itemInput.focus();
        transcriptView.textContent = data.text;
        setStatus("Transcript received. Review it before adding.");
      } catch (error) {
        setStatus("Could not send the transcript to the server. Your text is still shown above.");
      } finally {
        isSubmitting = false;
      }
    };
    return instance;
  }

  startButton.addEventListener("click", () => {
    if (recognition) recognition.abort();
    finalTranscript = "";
    transcriptView.textContent = "Listening…";
    shouldListen = true;
    recognition = createRecognition();
    setStatus("Listening… speak now", true);
    try {
      recognition.start();
    } catch (error) {
      shouldListen = false;
      setStatus("Could not start the microphone. Try again.");
    }
  });

  stopButton.addEventListener("click", () => {
    shouldListen = false;
    if (recognition) recognition.stop();
    setStatus("Finishing transcript…");
    stopButton.disabled = true;
  });

  languageSelect.addEventListener("change", () => {
    if (shouldListen && recognition) {
      shouldListen = false;
      recognition.stop();
      setStatus("Language changed. Start listening again.");
    }
  });
})();
