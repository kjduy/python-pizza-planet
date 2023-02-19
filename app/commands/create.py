from .command import Command


class CreateCommand(Command):
    def __init__(self, receiver, request):
        self.receiver = receiver
        self.request = request

    def execute(self):
        return self.receiver.create(self.request)
