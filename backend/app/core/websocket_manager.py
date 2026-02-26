from typing import Dict, List
from fastapi import WebSocket
import json
import asyncio
import redis.asyncio as redis

from app.core.config import settings


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis = redis.from_url(settings.REDIS_URL)

    async def connect(self, company_id: str, websocket: WebSocket):
        await websocket.accept()

        if company_id not in self.active_connections:
            self.active_connections[company_id] = []

        self.active_connections[company_id].append(websocket)

    def disconnect(self, company_id: str, websocket: WebSocket):
        self.active_connections[company_id].remove(websocket)

    async def broadcast(self, company_id: str, message: dict):
        if company_id in self.active_connections:
            for connection in self.active_connections[company_id]:
                await connection.send_text(json.dumps(message))

    async def publish(self, company_id: str, message: dict):
        await self.redis.publish(company_id, json.dumps(message))

    async def subscribe(self, company_id: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(company_id)

        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await self.broadcast(company_id, data)


manager = ConnectionManager()