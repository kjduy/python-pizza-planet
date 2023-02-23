from .base import BaseCommand


class GetAllCommand(BaseCommand):
    def execute(self):
        return self.receiver.get_all()
