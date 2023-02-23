from .base import BaseReceiver
from ..repositories.managers.beverage import BeverageManager


class BeverageReceiver(BaseReceiver):
    manager = BeverageManager
