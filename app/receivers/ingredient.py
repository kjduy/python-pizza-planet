from .base import BaseReceiver
from ..repositories.managers.ingredient import IngredientManager


class IngredientReceiver(BaseReceiver):
    manager = IngredientManager
