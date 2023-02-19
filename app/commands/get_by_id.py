from .command import Command


class GetByIdCommand(Command):
    def __init__(self, receiver, _id: int):
        self.receiver = receiver
        self._id = _id

    def execute(self):
        return self.receiver.get_by_id(self._id)
