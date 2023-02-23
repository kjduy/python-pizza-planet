from typing import List

from .base import BaseManager
from ..models import Beverage, Ingredient, Order, OrderDetail
from ..serializers.order import OrderSerializer


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, beverages: List[Beverage], ingredients: List[Ingredient]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all(
            list(
                map(
                    lambda beverage, ingredient: OrderDetail(
                        order_id=new_order._id,
                        beverage_id=beverage._id,
                        beverage_price=beverage.price,
                        ingredient_id=ingredient._id,
                        ingredient_price=ingredient.price
                    ),
                    beverages,
                    ingredients
                )
            )
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')
