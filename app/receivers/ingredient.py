from .base import BaseReceiver
from ..repositories.managers import IngredientManager


class IngredientReceiver(BaseReceiver):
    manager = IngredientManager
