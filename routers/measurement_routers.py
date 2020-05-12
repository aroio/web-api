import subprocess

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse

from models import Aroio
from routers import get_auth_aroio

router = APIRouter()

@router.websocket("/meassurement/socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
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
