import json
from .models import Homeegram, Node


class Homee:
    def __init__(self, client):
        self.client = client

    async def get_homeegrams(self):
        """Fetch all homeegrams."""
        await self.client.send("GET:homeegrams")
        response = await self.client.receive()
        data = json.loads(response)
        return [Homeegram.from_dict(hg) for hg in data.get("homeegrams", [])]

    async def play_homeegram(self, homeegram_id):
        """Start a homeegram."""
        await self.client.send(f"PUT:homeegrams/{homeegram_id}?play=1")

    async def enable_homeegram(self, homeegram_id):
        """Enable a homeegram."""
        await self.client.send(f"PUT:homeegrams/{homeegram_id}?enable=1")

    async def disable_homeegram(self, homeegram_id):
        """Disable a homeegram."""
        await self.client.send(f"PUT:homeegrams/{homeegram_id}?enable=0")

    async def get_nodes(self):
        """Fetch all nodes."""
        await self.client.send("GET:nodes")
        response = await self.client.receive()
        data = json.loads(response)
        return [Node.from_dict(node) for node in data.get("nodes", [])]
