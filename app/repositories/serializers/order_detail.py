from app.plugins import ma

from ..models import OrderDetail
from .beverage import BeverageSerializer
from .ingredient import IngredientSerializer


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):
    beverage = ma.Nested(BeverageSerializer)
    ingredient = ma.Nested(IngredientSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = ("beverage_price", "beverage", "ingredient_price", "ingredient")
