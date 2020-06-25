import subprocess
import time
import json
from models import (Command)
from fastapi import APIRouter, WebSocket
router = APIRouter()


def checkMic():
    return subprocess.run('./scripts/hasMic.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


@router.websocket("/meassurement/socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data_json = json.loads(data)

        if 'command' in data_json:
            print(data_json["command"])
            if data_json["command"] == "microphone_adjustment":
                micPlugged = 0
                while micPlugged == 0:
                    micPlugged = checkMic().returncode
                    if micPlugged == 1:
                        print('Mic is plugged')
                        await websocket.send_json(json.dumps(Command(command='mic_plugged', value=True).__dict__))

        await websocket.send_json(data)


@router.websocket("/meassurement/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in numbers:
            time.sleep(1)
            await websocket.send_json(i)
        await websocket.send_json(data)

# @router.websocket("/meassurement/socket")
# async def websocket_endpoint(websocket: WebSocket):
#     """WebSocket connection for emmitting data to the client"""
#     await websocket.accept()
#     while True:
#         command = await websocket.receive_text()
#         process = {
#             "MEASURE": ["scripts/measure.sh", "debug"]
#         }[command.upper()]
#         result = subprocess.run(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#         await websocket.send_text(f"{result.returncode}, {result.stdout}, {result.stderr}")
