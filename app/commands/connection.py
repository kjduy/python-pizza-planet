from .command import Command


class TestConnectionCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        return self.receiver.test_connection()