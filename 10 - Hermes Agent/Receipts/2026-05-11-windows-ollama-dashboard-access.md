Custom OpenAI-compatible endpoint configuration:



API base URL [e.g. https://api.example.com/v1]: http://192.168.7.170:11434

API key [optional]:



  Hint: Did you mean to add /v1 at the end?

  Most local model servers (Ollama, vLLM, llama.cpp) require it.

  e.g. http://192.168.7.170:11434/v1

  Add /v1? [Y/n]: y

  Updated URL: http://192.168.7.170:11434/v1



Verified endpoint via http://192.168.7.170:11434/v1/models (1 model(s) visible)

  Detected model: gemma4:latest

  Use this model? [Y/n]: y

Context length in tokens [leave blank for auto-detect]:

Display name [192.168.7.170:11434]: windows ollama

Default model set to: gemma4:latest (via http://192.168.7.170:11434/v1)

  💾 Saved to custom providers as "windows ollama" (edit in config.yaml)

codysumpter@Codys-MacBook-Pro ~ % hermes

Hermes Dashboard on iPhone (mac hermes)

- Started dashboard on Mac LAN:

  - URL: http://192.168.7.49:9119/

- Receipt:

  - Listening on *:9119

  - Local GET returns Hermes Dashboard HTML

- Open that URL from your iPhone on the same Wi-Fi.
