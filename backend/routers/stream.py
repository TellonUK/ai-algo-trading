import asyncio
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from services.ai_model import ai_model
from services.history_loader import OHLCData

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


def generate_mock_bar(symbol: str = "TSLA") -> OHLCData:
    base_time = datetime.now().replace(second=0, microsecond=0)
    
    import random
    base_price = 250.0 if symbol == "TSLA" else 175.0
    open_price = base_price + random.uniform(-5, 5)
    high_price = open_price + random.uniform(0, 3)
    low_price = open_price - random.uniform(0, 3)
    close_price = open_price + random.uniform(-2, 2)
    
    return OHLCData(
        timestamp=base_time.isoformat() + "Z",
        open=round(open_price, 2),
        high=round(high_price, 2),
        low=round(low_price, 2),
        close=round(close_price, 2)
    )


async def stream_data():
    while True:
        bar = generate_mock_bar()
        decision = ai_model.make_decision(bar)
        
        message = {
            "timestamp": bar.timestamp,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "decision": decision
        }
        
        await manager.broadcast(json.dumps(message))
        await asyncio.sleep(60)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    if len(manager.active_connections) == 1:
        asyncio.create_task(stream_data())
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)