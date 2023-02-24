from app.repositories.models import Order, OrderDetail
from app.seed.client_faker import ClientFaker


def create_pizza_items(model, faker, constant):
    items = list(
        map(
            lambda item: model(
                name=item,
                price=faker.pyfloat(right_digits=2, positive=True, max_value=10),
            ),
            constant,
        )
    )
    return items


def create_clients(faker):
    clients = list(
        map(
            lambda _: ClientFaker(
                name=faker.name(),
                dni=faker.random_int(min=10**9, max=(10**10) - 1),
                address=faker.address(),
                phone=faker.numerify("09########"),
            ),
            range(10),
        )
    )
    return clients


def generate_random_set(elements, num_details, faker):
    return set(
        map(lambda _: faker.random_element(elements=elements), range(num_details))
    )


def create_order(order_id, clients, ingredients, beverages, sizes, faker):
    client = faker.random_element(elements=clients)
    client_name = client.name
    client_dni = client.dni
    client_address = client.address
    client_phone = client.phone
    date = faker.date_time_between(start_date="-1y", end_date="now")

    num_details = faker.random_int(min=1, max=5)
    ingredient_set = generate_random_set(ingredients, num_details, faker)
    beverage_set = generate_random_set(beverages, num_details, faker)

    order_details = []
    order_details = list(
        map(
            lambda ingredient, beverage: OrderDetail(
                ingredient_price=ingredient.price,
                beverage_price=beverage.price,
                ingredient=ingredient,
                beverage=beverage,
                order_id=order_id + 1,
            ),
            ingredient_set,
            beverage_set,
        )
    )

    total_price = sum(
        detail.beverage_price + detail.ingredient_price for detail in order_details
    )
    size = faker.random_element(elements=sizes)
    size_price = size.price
    total_price += size_price
    round_total_price = round(total_price, 2)

    orders = Order(
        client_name=client_name,
        client_dni=client_dni,
        client_address=client_address,
        client_phone=client_phone,
        date=date,
        total_price=round_total_price,
        size=size,
        detail=order_details,
    )

    return orders
