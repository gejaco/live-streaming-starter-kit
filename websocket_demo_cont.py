from fastapi import FastAPI, WebSocket
import asyncio
import os
import time
import shutil

app = FastAPI()

TRANSCRIPT_PATH = "transcript.txt"
ARCHIVE_DIR = "archive"

# Ensure archive directory exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    last_sent_time = 0

    try:
        while True:
            # Check if new transcript file exists
            if os.path.exists(TRANSCRIPT_PATH):
                # Get the file's creation/modification time
                file_mtime = os.path.getmtime(TRANSCRIPT_PATH)

                # Only send if it's newer than the last sent
                if file_mtime > last_sent_time:
                    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
                        transcript = f.read()

                    # Send to the frontend
                    await websocket.send_text(transcript)
                    print(f"[WS] Sent transcript at {time.strftime('%X')}")

                    # Update last sent time
                    last_sent_time = file_mtime

                    # Archive file so next transcript will be new
                    ts = int(time.time())
                    shutil.move(TRANSCRIPT_PATH, f"{ARCHIVE_DIR}/transcript_{ts}.txt")

            await asyncio.sleep(0.5)  # Polling interval

    except Exception as e:
        print(f"[WS] Connection closed or error: {e}")
