from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/roster/{company_id}")
async def roster_ws(websocket: WebSocket, company_id: str):

    await manager.connect(company_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Publish to Redis
            await manager.publish(company_id, data)

    except WebSocketDisconnect:
        manager.disconnect(company_id, websocket)