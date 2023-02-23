from ..repositories.managers.ingredient import IngredientManager
from .base import BaseReceiver


class IngredientReceiver(BaseReceiver):
    manager = IngredientManager
