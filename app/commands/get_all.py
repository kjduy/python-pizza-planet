from .command import Command


class GetAllCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        return self.receiver.get_all()
