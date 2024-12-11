import asyncio
import base64
import hashlib
import aiohttp
import websockets
import json

class HomeeClient:
    """Client to interact with the Homee API and WebSocket, mimicking pymee."""

    def __init__(self, host, username, password):
        """Initialize the Homee client."""
        self.host = host
        self.username = username
        self.password = password
        self.token = None
        self.websocket = None
        self.nodes = []  # Stores nodes (devices)
        self.attributes = []  # Stores attributes of nodes
        self.groups = []  # Stores groups
        self.homeegrams = []  # Stores homeegrams
        self.user = None  # Stores user information
        self.connected = False  # Connection status

    def _hash_password(self):
        """Hash the password using SHA512."""
        return hashlib.sha512(self.password.encode()).hexdigest()

    async def get_token(self):
        """Authenticate with Homee and retrieve the access token."""
        hashed_password = self._hash_password()
        combined_string = f"{self.username}:{hashed_password}"
        base64_string = base64.b64encode(combined_string.encode()).decode()

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64_string}"
        }

        params = (
            "device_name=DevApp&"
            "device_hardware_id=PythonClient&"
            "device_os=5&"
            "device_type=4&"
            "device_app=0"
        )

        url = f"http://{self.host}:7681/access_token"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, headers=headers) as response:
                if response.status == 200:
                    response_text = await response.text()
                    key_value_pairs = dict(pair.split('=') for pair in response_text.split('&'))
                    self.token = key_value_pairs.get("access_token")
                else:
                    raise Exception(f"Failed to get token: {response.status}")

    async def connect(self):
        """Connect to the Homee WebSocket and initialize data."""
        if not self.token:
            raise Exception("Token is not available. Call `get_token` first.")

        ws_url = f"ws://{self.host}:7681/connection?access_token={self.token}"

        try:
            self.websocket = await websockets.connect(
                ws_url,
                subprotocols=["v2"]
            )
            self.connected = True
            print("WebSocket connection established.")
            await self.initialize_homee_data()
            asyncio.create_task(self._listen_to_websocket())
        except Exception as e:
            raise Exception(f"WebSocket connection failed: {e}")

    async def initialize_homee_data(self):
        """Send initial commands to Homee WebSocket."""
        await self.websocket.send("get:nodes")
        await self.websocket.send("get:groups")
        await self.websocket.send("get:homeegrams")
        await self.websocket.send("get:user")

    async def _listen_to_websocket(self):
        """Listen to incoming WebSocket messages and process them."""
        try:
            async for message in self.websocket:
                self._process_message(message)
        except Exception as e:
            print(f"Error listening to WebSocket: {e}")

    def _process_message(self, message):
        """Process incoming WebSocket messages."""
        try:
            data = json.loads(message)
            if "nodes" in data:
                self.nodes = data["nodes"]
            if "attributes" in data:
                self.attributes = data["attributes"]
            if "groups" in data:
                self.groups = data["groups"]
            if "homeegrams" in data:
                self.homeegrams = data["homeegrams"]
            if "user" in data:
                self.user = data["user"]
            print(f"Processed message: {data}")
        except json.JSONDecodeError:
            print(f"Failed to decode message: {message}")

    async def get_nodes(self):
        """Return a list of nodes (devices)."""
        return self.nodes

    async def get_attributes(self):
        """Return a list of attributes for all nodes."""
        return self.attributes

    async def get_groups(self):
        """Return a list of groups."""
        return self.groups

    async def get_homeegrams(self):
        """Return a list of homeegrams."""
        return self.homeegrams

    async def get_user(self):
        """Return user information."""
        return self.user

    async def send_command(self, command):
        """Send a raw command to the WebSocket."""
        if not self.websocket:
            raise Exception("WebSocket is not connected.")
        await self.websocket.send(command)

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print("WebSocket connection closed.")

    async def start_homeegram(self, homeegram_id):
        """Start a Homeegram."""
        command = f"put:homeegrams/{homeegram_id}?play=1"
        await self.send_command(command)

# Example usage
# client = HomeeClient("192.168.178.39", "username", "password")
# asyncio.run(client.get_token())
# asyncio.run(client.connect())
# asyncio.run(client.start_homeegram(123))
# asyncio.run(client.close())
