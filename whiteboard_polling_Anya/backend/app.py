from fastapi import FastAPI, HTTPException, Body
from config import ROOM_ID, FILTERS
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from cpp_module.filter import apply_filter_cpp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()
_store = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Константа для ROOM_ID
ROOM_ID = "room_6027"

room_commands = {}


@app.post("/draw/{room_id}")
def post_draw(room_id: str, cmd: dict):
    room = room_commands.setdefault(room_id, [])
    room.append(cmd)
    return {"status": "ok"}

@app.get("/draw/{room_id}")
def get_draw(room_id: str):
    return room_commands.get(room_id, [])

# Обробка малювання на дошці
@app.post("/filter/{room_id}")
def filter_image(room_id: str, payload: dict):
    if room_id != ROOM_ID:
        raise HTTPException(status_code=404, detail="Room not found")
    
    image_data = payload.get("image_data")
    filter_name = payload.get("filter_name")
    width = payload.get("width")
    height = payload.get("height")

    if not image_data:
        raise HTTPException(status_code=400, detail="No image data provided")
    if not width or not height:
        raise HTTPException(status_code=400, detail="Missing width or height")

    print(f"Filter requested: {filter_name}")
    print(f"Image data length: {len(image_data)}")
    print(f"Dimensions: {width}x{height}")

    filtered = apply_filter_cpp(image_data, width, height, filter_name)

    print(f"Filtered data length: {len(filtered)}")

    return {"image_data": filtered}

