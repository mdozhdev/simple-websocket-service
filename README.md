# Simple WebSocket Audio Transcription Service

A lightweight WebSocket service built with Starlette that receives audio chunks, transcribes them using OpenAI Whisper, and streams results back in near real-time.

## Features

- WebSocket-based audio streaming
- Real-time transcription using OpenAI Whisper API
- Audio file storage
- Docker support
- CLI test client

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key with Whisper access

## Setup

### 1. Configure Environment

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.

### 2. Using Docker (Recommended)

Build and run the service:

```bash
docker-compose up --build
```

The service will be available at `ws://localhost:8000/ws`

### 3. Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Export your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

Run the service:

```bash
python main.py
```

## Usage

### Using the CLI Test Client

The included test client sends audio files to the service:

```bash
python test_client.py path/to/audio.wav
```

Options:
- `--uri`: WebSocket server URI (default: `ws://localhost:8000/ws`)
- `--chunk-size`: Chunk size in bytes (default: 4096)

Example:

```bash
python test_client.py sample.wav --chunk-size 8192
```

### WebSocket Protocol

The service accepts WebSocket connections at `/ws`:

1. **Connect** to `ws://localhost:8000/ws`
2. **Receive** connection confirmation
3. **Send** audio chunks as binary data
4. **Receive** transcription results in JSON format:
   ```json
   {
     "type": "transcription",
     "text": "transcribed text here"
   }
   ```
5. **Send** text message `"END"` to finalize and save the audio file
6. **Receive** confirmation with saved file path

### Response Types

- `status`: Connection status or completion messages
- `transcription`: Transcribed text from audio chunk
- `error`: Error messages


## Audio Files

Audio files are automatically saved to the `audio_files/` directory with timestamps:
- Format: `audio_YYYYMMDD_HHMMSS.wav`
- Files are saved when the client sends "END" or disconnects

## Development

The service uses:
- **Starlette**: Lightweight ASGI framework
- **Uvicorn**: ASGI server
- **OpenAI**: Whisper API integration
- **websockets**: WebSocket client library (for test client)

## Notes

- Service do pseudostreaming - it runs accumulated buffer multiple times increasing request size
- The service processes each audio chunk independently through Whisper
- Temporary files are created for API calls and cleaned up immediately
- All audio chunks are stored in memory and saved at the end
- The service supports multiple concurrent connections
