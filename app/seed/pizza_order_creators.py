from app.repositories.models import OrderDetail, Order
from app.seed.client_faker import ClientFaker


def create_pizza_items(model, faker, constant):
    items = list(
        map(
            lambda item: model(
                name=item,
                price=faker.pyfloat(right_digits=2, positive=True, max_value=10)
            ),
            constant
        )
    )
    return items


def create_clients(faker):
    clients = list(
        map(
            lambda _: ClientFaker(
                name=faker.name(),
                dni=faker.random_int(min=10**9, max=(10**10)-1),
                address=faker.address(),
                phone=faker.numerify('09########')
            ),
            range(10)
        )
    )
    return clients



def create_order(order_id, clients, ingredients, beverages, sizes, faker):
    client = faker.random_element(elements=clients)
    client_name = client.name
    client_dni = client.dni
    client_address = client.address
    client_phone = client.phone
    date = faker.date_between(start_date='-1y', end_date='today')

    ingredient = faker.random_element(elements=ingredients)
    ingredient_price = ingredient.price

    beverage = faker.random_element(elements=beverages)
    beverage_price = beverage.price

    size = faker.random_element(elements=sizes)
    size_price = size.price

    total_price = round(beverage_price + ingredient_price + size_price, 2)

    order_details = []
    order_detail = OrderDetail(
        ingredient_price=ingredient_price,
        beverage_price=beverage_price,
        ingredient=ingredient,
        beverage=beverage,
        order_id=order_id+1
    )
    order_details.append(order_detail)

    orders = Order(
        client_name=client_name,
        client_dni=client_dni,
        client_address=client_address,
        client_phone=client_phone,
        date=date,
        total_price=total_price,
        size=size,
        detail=order_details
    )
    
    return orders
