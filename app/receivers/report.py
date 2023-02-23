from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers.report import ReportManager


class ReportReceiver:
    manager = ReportManager

    @classmethod
    def get_report(cls):
        try:
            return cls.manager.get_report(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
