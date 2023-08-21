from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket</title>
    </head>
    <body>
        <h2>Enter text:</h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:5000/ws")
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
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


@app.get("/")
async def get():
    return HTMLResponse(html)


# Создаем список WebSocket-соединений
ws_connections = []


# Обработчик WebSocket-соединений
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Добавляем новое соединение в список
    ws_connections.append(websocket)

    # Отправка стабильного формата ответа

    while True:
        # Логика для обновления данных в формате, который нужно отправить
        data = await websocket.receive_text()
        data = {"message": data}

        # Отправка данных всем клиентам в формате JSON
        for ws in ws_connections:
            await ws.send_json(data)
