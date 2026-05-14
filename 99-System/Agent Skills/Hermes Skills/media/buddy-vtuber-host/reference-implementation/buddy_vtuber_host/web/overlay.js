const buddy = document.getElementById("buddy");
const caption = document.getElementById("caption");
const voice = document.getElementById("voice");

let activeVisemes = [];
let activeStart = 0;
let rafId = null;

function setState(state) {
  buddy.classList.remove("idle", "thinking", "speaking", "listening", "error");
  buddy.classList.add(state || "idle");
  if (state === "idle") {
    buddy.dataset.mouth = "closed";
  }
}

function setCaption(text) {
  caption.textContent = text || "";
  caption.classList.toggle("visible", Boolean(text));
}

function applyViseme(mouth) {
  buddy.dataset.mouth = mouth || "closed";
}

function startVisemes(visemes) {
  activeVisemes = Array.isArray(visemes) ? visemes : [];
  activeStart = performance.now();

  if (rafId) {
    cancelAnimationFrame(rafId);
  }

  const tick = () => {
    const elapsed = (performance.now() - activeStart) / 1000;
    let current = activeVisemes[0];

    for (const frame of activeVisemes) {
      if (frame.t <= elapsed) {
        current = frame;
      } else {
        break;
      }
    }

    if (current) {
      applyViseme(current.mouth);
    }

    if (!voice.paused && !voice.ended) {
      rafId = requestAnimationFrame(tick);
    } else {
      applyViseme("closed");
      rafId = null;
    }
  };

  rafId = requestAnimationFrame(tick);
}

async function handleSpeech(event) {
  const text = event.text || "";
  const audioUrl = event.audio_url;
  setState("speaking");
  setCaption(text);

  if (audioUrl) {
    voice.src = `${audioUrl}?v=${Date.now()}`;
    voice.onplay = () => startVisemes(event.visemes || []);
    voice.onended = () => {
      applyViseme("closed");
      setState("idle");
      window.setTimeout(() => setCaption(""), 900);
    };

    try {
      await voice.play();
    } catch (err) {
      console.warn("[buddy-overlay] audio autoplay blocked or failed:", err);
      startVisemes(event.visemes || []);
      window.setTimeout(() => {
        applyViseme("closed");
        setState("idle");
        setCaption("");
      }, 2200);
    }
  } else {
    startVisemes(event.visemes || []);
    window.setTimeout(() => {
      applyViseme("closed");
      setState("idle");
      setCaption("");
    }, Math.max(1600, text.length * 38));
  }
}

function connectEvents() {
  const events = new EventSource("/events");

  events.addEventListener("hello", () => {
    console.log("[buddy-overlay] connected");
  });

  events.addEventListener("state", (message) => {
    const event = JSON.parse(message.data);
    setState(event.state || "idle");
    if (event.state === "thinking") {
      setCaption("thinking...");
    }
    if (event.state === "idle" && voice.paused) {
      window.setTimeout(() => setCaption(""), 400);
    }
  });

  events.addEventListener("speech", (message) => {
    const event = JSON.parse(message.data);
    handleSpeech(event);
  });

  events.addEventListener("chat", (message) => {
    const event = JSON.parse(message.data);
    console.log("[buddy-overlay] chat", event.author, event.text);
  });

  events.addEventListener("error", (message) => {
    const event = JSON.parse(message.data);
    console.error("[buddy-overlay]", event.message);
    setState("error");
    setCaption("Oops. Buddy hit a tiny snag.");
  });

  events.onerror = () => {
    console.warn("[buddy-overlay] event stream disconnected; browser will retry");
  };
}

setState("idle");
connectEvents();
