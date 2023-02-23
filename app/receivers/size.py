from .base import BaseReceiver
from ..repositories.managers.size import SizeManager


class SizeReceiver(BaseReceiver):
    manager = SizeManager
