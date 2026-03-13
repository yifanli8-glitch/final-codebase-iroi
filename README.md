# DOGU Robot Project

This project provides a PyQt-based robot UI with realtime voice interaction, lab QA support, and navigation-related command handling.

## 1) Project Structure

```text
DOOOGU/
├── robot_ui.py                 # Main app entry point
├── tts_player.py               # Text-to-speech playback helper
├── command_parser.py           # Parse spoken navigation commands
├── ros_command.py              # Send navigation/control commands via ROS
├── requirements.txt            # Python dependencies
├── model/                      # Wake-word model files
├── ui/                         # UI panels, widgets, assets
├── voice/                      # Realtime voice stack + RAG retrieval
│   ├── realtime_voice_assistant_rag.py
│   ├── realtime_fc/
│   ├── local_peer.py
│   ├── mic_stream_arecord.py
│   ├── audio_distributor.py
│   ├── rag_retriever.py
│   └── rag_config.py
├── scripts/                    # Optional helpers (camera stream, setup)
│   ├── camera_stream_server.py
│   ├── start_with_camera.py
│   └── install_audio_deps.sh
└── docs/                       # Course and implementation documentation
```

## 2) How To Run

### Prerequisites

- Python 3.10+ recommended
- A valid OpenAI API key available in your local config/environment
- Audio input/output support (`arecord`, `aplay`, and optional `mpg123`)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the main application

```bash
python3 robot_ui.py --voice-mode realtime_tts
```

### Voice mode options

- `realtime_tts` (recommended): realtime session + local high-quality TTS playback
- `realtime`: realtime session with direct realtime audio output
- `legacy`: older record/transcribe/respond pipeline

## 3) What To Expect After Running

After startup, the PyQt window opens and initializes voice services.

- The app prints the selected voice mode in terminal output.
- If audio device and API key checks pass, realtime assistant starts.
- Wake-word flow is enabled; saying the wake word triggers lab interaction flow.
- In QA flow, speech is transcribed, responses are shown in UI, and TTS playback is produced (for `realtime_tts`).
- Navigation-related parsing/dispatch remains available through:
  - `command_parser.py`
  - `ros_command.py`
  - map UI via `ui/panels/map_panel.py` and `ui/Map.png`

## 4) Keyboard Controls

- `1` Default
- `2` I AM COMING
- `3` I AM LISTENING
- `4` FOLLOW ME
- `5` Status
- `6` Map
- `7` Camera
- `8` Conversation
- `9` Lab Select
- `0` Lab Detail
- `F/F11` Fullscreen toggle
- `ESC` Exit
