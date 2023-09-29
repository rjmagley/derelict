class Inventory():

    def __init__(self, size: int = 10):
        self.items = []
        self.size = size

    @property
    def space_remaining(self) -> bool:
        return (self.size - len(self.items)) > 0