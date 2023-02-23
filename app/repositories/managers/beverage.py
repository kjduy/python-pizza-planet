from typing import Sequence

from ..models import Beverage
from ..serializers.beverage import BeverageSerializer
from .base import BaseManager


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )
