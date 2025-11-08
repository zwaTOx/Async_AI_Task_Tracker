from fastapi import WebSocket

from src.database import async_session
from src.project.repository import ProjectRepository
from src.user_project_association.repository import UserProjectAssociationRepository


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            existing_connection = self.active_connections[user_id]
            try:
                await existing_connection.close()
            except Exception as e:
                pass
            finally:
                del self.active_connections[user_id]
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, payload: dict):
        if self.active_connections.get(user_id):
            await self.active_connections[user_id].send_json(payload)

    async def broadcast_to_project(self, project_id: int, message_data: dict):
        disconnected_users = []
        async with async_session() as session:
            try:
                chat_user_repo = UserProjectAssociationRepository(session)
                chat_members = await chat_user_repo.get_project_memberships(project_id)
                
                for member in chat_members:
                    user_id = member.user_id
                    print(f'id: {user_id}')
                    if user_id in self.active_connections:
                        try:
                            print(f'Sended')
                            await self.active_connections[user_id].send_json(message_data)
                        except Exception:
                            print(f'Dissconnect')
                            disconnected_users.append(user_id)
            finally:
                await session.close()
        
        for user_id in disconnected_users:
            if user_id in self.active_connections:
                del self.active_connections[user_id]

ws_manager = ConnectionManager()