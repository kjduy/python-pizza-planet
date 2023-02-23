from .base import BaseCommand


class TestConnectionCommand(BaseCommand):
    def execute(self):
        return self.receiver.test_connection()
