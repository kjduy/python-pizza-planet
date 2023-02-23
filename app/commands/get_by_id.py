from .base import BaseCommand


class GetByIdCommand(BaseCommand):
    def __init__(self, receiver, _id: int):
        super().__init__(receiver)
        self._id = _id

    def execute(self):
        return self.receiver.get_by_id(self._id)
