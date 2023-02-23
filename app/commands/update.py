from .base import BaseCommand


class UpdateCommand(BaseCommand):
    def __init__(self, receiver, request):
        super().__init__(receiver)
        self.request = request

    def execute(self):
        return self.receiver.update(self.request)
