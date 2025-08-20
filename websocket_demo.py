from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import test_suite
import os

app = FastAPI()
TRANSCRIPT_PATH = "transcripts.txt"

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # (Instead of this, stream live transcription results from your ASR model)
    transcript_chunks = [
        "Hello, this is",
        " a live transcription",
        " being sent",
        " in real time!"
    ]
    print("Socket connection established, sending transcript chunks...")
    # Wait until transcript file exists
    while not os.path.exists(TRANSCRIPT_PATH):
        print("Waiting for transcript file to be created...", os.path.exists(TRANSCRIPT_PATH))
        await asyncio.sleep(0.5)
    print("Transcript file found, sending contents...")
    # Read the transcript
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        transcript = f.read()
    
    await websocket.send_text(transcript)

    # Delete after sending to avoid re-sending old transcript
    try:
        os.remove(TRANSCRIPT_PATH)
    except OSError as e:
        print(f"Error deleting transcript file: {e}")
            
    print("Transcript sent.")
    # for chunk in transcript_chunks:
    #     await asyncio.sleep(1)  # Simulate delay for demonstration
    #     await websocket.send_text(chunk)
    await websocket.close()
