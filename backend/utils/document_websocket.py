from fastapi import WebSocket, WebSocketDisconnect
from uuid import UUID
from typing import Dict, Set
from starlette.websockets import WebSocketState

from utils.uow import UnitOfWork
from logging import getLogger


class DocumentConnectionService:
    def __init__(self):
        self.active_documents: Dict[UUID, Set[WebSocket]] = {}
        self.uow = UnitOfWork()
        self.logger = getLogger()

    async def connect(self, document_id: UUID, websocket: WebSocket):
        await websocket.accept()

        if document_id not in self.active_documents:
            self.active_documents[document_id] = set()
        self.active_documents[document_id].add(websocket)

        async with self.uow.start():
            document = await self.uow.documents.get_by_id(document_id=document_id)

        if document.yjs_updates:
            await websocket.send_bytes(document.yjs_updates)

        self.logger.info(f"К документу {document.file_path} подключился новый пользователь.\n"
                         f"Всего подключений к этому документу: {len(self.active_documents[document_id])}")

        try:
            while True:
                data = await websocket.receive_bytes()
                disconnected = []
                for connection in self.active_documents[document_id]:
                    if connection.client_state != WebSocketState.CONNECTED:
                        disconnected.append(connection)
                        continue
                    if connection != websocket:
                        await connection.send_bytes(data)

                for connection in disconnected:
                    if connection in self.active_documents[document_id]:
                        self.active_documents[document_id].remove(connection)
        except WebSocketDisconnect:
            pass
        finally:
            if document_id in self.active_documents:
                self.active_documents[document_id].discard(websocket)


document_connection_manager = DocumentConnectionService()
