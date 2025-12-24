#!/usr/bin/env python3
import asyncio
import websockets
import sys
import argparse
from pathlib import Path


async def send_audio(uri: str, audio_file: str, chunk_size: int = 4096):
    """
    Send audio file to WebSocket server in chunks

    Args:
        uri: WebSocket server URI
        audio_file: Path to audio file
        chunk_size: Size of chunks to send (default 4096 bytes)
    """
    audio_path = Path(audio_file)

    if not audio_path.exists():
        print(f"Error: Audio file '{audio_file}' not found")
        return

    print(f"Connecting to {uri}...")

    async with websockets.connect(uri) as websocket:
        print("Connected!")

        # Receive connection confirmation
        response = await websocket.recv()
        print(f"Server: {response}")

        # Read and send audio file in chunks
        with open(audio_path, "rb") as f:
            chunk_num = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                chunk_num += 1
                print(f"Sending chunk {chunk_num} ({len(chunk)} bytes)...")
                await websocket.send(chunk)

                # Wait for transcription response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=0.2)
                    print(f"Server response: {response}")
                except asyncio.TimeoutError:
                    print("Waiting for response...")

        # Send END signal
        print("Sending END signal...")
        await websocket.send("END")

        # Wait for final confirmation
        response = await websocket.recv()
        print(f"Server: {response}")


def main():
    parser = argparse.ArgumentParser(
        description="Test client for WebSocket audio transcription service"
    )
    parser.add_argument(
        "audio_file",
        help="Path to audio file to transcribe"
    )
    parser.add_argument(
        "--uri",
        default="ws://localhost:8000/ws",
        help="WebSocket server URI (default: ws://localhost:8000/ws)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=4096,
        help="Chunk size in bytes (default: 4096)"
    )

    args = parser.parse_args()

    try:
        asyncio.run(send_audio(args.uri, args.audio_file, args.chunk_size))
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
