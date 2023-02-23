from .base import BaseCommand


class GetReportCommand(BaseCommand):
    def execute(self):
        return self.receiver.get_report()
