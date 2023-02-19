from .base import BaseReceiver
from ..repositories.managers import BeverageManager


class BeverageReceiver(BaseReceiver):
    manager = BeverageManager
