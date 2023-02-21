import pytest
import subprocess

from flask.cli import FlaskGroup
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

from app import flask_app
from app.plugins import db
from app.repositories.models import Beverage, Ingredient, Order, OrderDetail, Size


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)

seeder = FlaskSeeder()
seeder.init_app(flask_app, db)


@manager.command('delete_db', with_appcontext=False)
def delete_db():
    subprocess.run('python ./manage.py db downgrade', shell=True)
    subprocess.run('python ./manage.py db upgrade', shell=True)


@manager.command('populate_db', with_appcontext=False)
def populate_db():
    subprocess.run('python ./manage.py seed run --root app/seed', shell=True)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])


if __name__ == '__main__':
    manager()
