class Homeegram:
    """Represents a Homeegram."""

    def __init__(self, id, name, active, state):
        self.id = id
        self.name = name
        self.active = active
        self.state = state

    def __repr__(self):
        return f"<Homeegram id={self.id} name={self.name} active={self.active} state={self.state}>"

    @classmethod
    def from_dict(cls, data):
        """Create a Homeegram instance from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            active=data["active"],
            state=data["state"],
        )


class Node:
    """Represents a Node (device) in the homee system."""

    def __init__(self, id, name, available):
        self.id = id
        self.name = name
        self.available = available

    def __repr__(self):
        return f"<Node id={self.id} name={self.name} available={self.available}>"

    @classmethod
    def from_dict(cls, data):
        """Create a Node instance from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            available=data["available"],
        )
