from ..commands.command import Command


class Invoker:
    def __init__(self, command: Command):
        self.command = command

    def execute(self):
        return self.command.execute()
