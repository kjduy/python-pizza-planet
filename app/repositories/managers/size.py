from ..models import Size
from ..serializers.size import SizeSerializer
from .base import BaseManager


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer
