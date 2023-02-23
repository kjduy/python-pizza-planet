from .base import BaseCommand


class CreateCommand(BaseCommand):
    def __init__(self, receiver, request):
        super().__init__(receiver)
        self.request = request

    def execute(self):
        return self.receiver.create(self.request)
