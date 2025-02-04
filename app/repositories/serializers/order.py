from app.plugins import ma

from ..models import Order
from .order_detail import OrderDetailSerializer
from .size import SizeSerializer


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            "_id",
            "client_name",
            "client_dni",
            "client_address",
            "client_phone",
            "date",
            "total_price",
            "size",
            "detail",
        )
