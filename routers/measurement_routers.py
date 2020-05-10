import subprocess

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse

from models import Aroio
from routers import get_auth_aroio


router = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
            <button>Open</button>
            <button>Close</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:4200/socket");
            ws.onmessage = retrieveEvent(event.data);

            function retrieveEvent(data) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)



@router.websocket("/socket")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for emmitting data to the client"""
    await websocket.accept()
    while True:
        command = await websocket.receive_text()
        process = {
            "MEASURE": ["scripts/measure.sh", "debug"]
        }[command.upper()]
        result = subprocess.run(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        await websocket.send_text(f"{result.returncode}, {result.stdout}, {result.stderr}")
    
