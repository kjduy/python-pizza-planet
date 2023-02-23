from typing import Tuple

from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers.index import IndexManager


class IndexReceiver:
    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        try:
            IndexManager.test_connection()
            return True, ""
        except (SQLAlchemyError, RuntimeError) as ex:
            return False, str(ex)
