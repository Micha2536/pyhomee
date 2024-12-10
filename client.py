import asyncio
import websockets
import json


class HomeeClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    async def connect(self):
        """Establish WebSocket connection."""
        uri = f"ws://{self.host}/connection"
        self.connection = await websockets.connect(uri)

        auth_message = json.dumps({
            "action": "authenticate",
            "username": self.username,
            "password": self.password,
        })
        await self.connection.send(auth_message)

    async def send(self, message):
        """Send a raw message to the WebSocket."""
        if self.connection is None:
            raise ConnectionError("Not connected to homee.")
        await self.connection.send(message)

    async def receive(self):
        """Receive a raw message from the WebSocket."""
        if self.connection is None:
            raise ConnectionError("Not connected to homee.")
        return await self.connection.recv()

    async def close(self):
        """Close the WebSocket connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None
