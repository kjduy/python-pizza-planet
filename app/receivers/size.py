from .base import BaseReceiver
from ..repositories.managers import SizeManager


class SizeReceiver(BaseReceiver):
    manager = SizeManager
