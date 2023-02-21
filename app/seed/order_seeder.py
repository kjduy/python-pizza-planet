from datetime import datetime, timedelta
from faker import Faker
from flask_seeder import Seeder

from app.plugins import db
from app.repositories.models import Beverage, Ingredient, Size
from app.seed.pizza_constants import *
from app.seed.pizza_order_creators import *


class OrderSeeder(Seeder):
    def run(self):
        faker = Faker()

        ingredients = create_pizza_items(Ingredient, faker, INGREDIENTS)
        db.session.add_all(ingredients)

        sizes = create_pizza_items(Size, faker, SIZES)
        db.session.add_all(sizes)

        beverages = create_pizza_items(Beverage, faker, BEVERAGES)
        db.session.add_all(beverages)

        clients = create_clients(faker)

        order = list(map(lambda order_id: create_order(order_id, clients, ingredients, beverages, sizes, faker), range(100)))
        db.session.add_all(order)

        db.session.commit()
