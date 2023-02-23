from ..repositories.managers.beverage import BeverageManager
from .base import BaseReceiver


class BeverageReceiver(BaseReceiver):
    manager = BeverageManager
