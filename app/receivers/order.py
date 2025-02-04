from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import (
    BeverageManager,
    IngredientManager,
    OrderManager,
    SizeManager,
)
from .base import BaseReceiver


class OrderReceiver(BaseReceiver):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(size_price: float, beverages: list, ingredients: list):
        price = (
            size_price
            + sum(map(lambda beverage: beverage.price, beverages))
            + sum(map(lambda ingredient: ingredient.price, ingredients))
        )
        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        if not check_required_keys(cls.__required_info, current_order):
            return "Invalid order payload", None

        size_id = current_order.get("size_id")
        size = SizeManager.get_by_id(size_id)

        if not size:
            return "Invalid size for Order", None

        beverage_ids = current_order.pop("beverages", [])
        ingredient_ids = current_order.pop("ingredients", [])
        try:
            beverages = BeverageManager.get_by_id_list(beverage_ids)
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            price = cls.calculate_order_price(size.get("price"), beverages, ingredients)
            order_with_price = {**current_order, "total_price": price}
            return cls.manager.create(order_with_price, beverages, ingredients), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
