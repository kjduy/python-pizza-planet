from ..repositories.managers.size import SizeManager
from .base import BaseReceiver


class SizeReceiver(BaseReceiver):
    manager = SizeManager
