class Status:
    id: int
    status: str

    def __init__(self, id, status):
        self.id = id
        self.status = status

    def value(self):
        return {"id": self.id, "status": self.status}