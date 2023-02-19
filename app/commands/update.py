from .command import Command


class UpdateCommand(Command):
    def __init__(self, receiver, request):
        self.receiver = receiver
        self.request = request

    def execute(self):
        return self.receiver.update(self.request)
