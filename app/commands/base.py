from .command import Command


class BaseCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        raise NotImplementedError('The execute function must be implemented')
