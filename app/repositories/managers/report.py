from datetime import datetime
from sqlalchemy.sql import text

from app.plugins import db
from .base import BaseManager
from ..models import Ingredient, Order, OrderDetail


class ReportManager(BaseManager):
    @classmethod
    def get_report(cls):
        return {
            'most_requested_ingredient': cls.get_most_requested_ingredient(),
            'month_with_more_revenue': cls.get_month_with_more_revenue(),
            'best_customers': cls.get_best_customers(),
        }

    @classmethod
    def get_most_requested_ingredient(cls):
        most_requested_ingredient = cls.session.query(
            OrderDetail.ingredient_id,
            Ingredient.name,
            db.func.count(OrderDetail.ingredient_id).label('num_requested')
        ).join(Ingredient).group_by(OrderDetail.ingredient_id).order_by(text('num_requested DESC')).first()

        return {'name': most_requested_ingredient.name, 'num_requested': most_requested_ingredient.num_requested}

    @classmethod
    def get_month_with_more_revenue(cls):
        month_with_more_revenue = cls.session.query(
            db.func.strftime('%m', Order.date).label('month'),
            db.func.sum(Order.total_price).label('revenue')
        ).group_by('month').order_by(text('revenue DESC')).first()

        month_name = datetime.strptime(month_with_more_revenue.month, '%m').strftime('%B')

        return {'month': month_name, 'revenue': round(month_with_more_revenue.revenue, 2)}

    @classmethod
    def get_best_customers(cls):
        best_customers = cls.session.query(
            Order.client_name,
            Order.client_dni,
            Order.client_address,
            Order.client_phone,
            db.func.count(Order._id).label('num_orders')
        ) \
        .group_by(Order.client_name, Order.client_dni, Order.client_address, Order.client_phone) \
        .order_by(text('num_orders DESC')) \
        .limit(3) \
        .all()

        best_customers = list(map(lambda client: {
            "client_name": client[0],
            "client_dni": client[1],
            "client_address": client[2],
            "client_phone": client[3],
            "num_orders": client[4]
        }, best_customers))

        return {'customers': best_customers}
