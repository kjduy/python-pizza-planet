from sqlalchemy.sql import column, text

from .base import BaseManager


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()
