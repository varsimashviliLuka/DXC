from flask.cli import with_appcontext
import click
from src.extensions import db
from src.models import User
import random



@click.command("init_db")
@with_appcontext
def init_db():
    # აპლიკაციის შექმნისას თავდაპირველი ბრძანებები ნ1
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")


@click.command("populate_db")
@with_appcontext
def populate_db():
    # აპლიკაციის შექმნისას თავდაპირველი ბრძანებები ნ2
    click.echo("Creating User")
    admin_user = User (
        email="varsimashvili.official@gmail.com",
        password="LUKAluka123",
        phone_number="592159199",
        personal_number="01124096118",
        identification_number=random.randint(100000, 999999),
        role="admin"
    )

    admin_user.create()
    click.echo("First Tables Created")

@click.command("insert_db")
@with_appcontext
def insert_db():
    # Insert-ით რაც გინდა ის ქენი
    test_user = User (
        email="testmail@gmail.com",
        password="LUKAluka123",
        phone_number="592159194",
        personal_number="01124096418",
        identification_number=random.randint(100000, 999999),
        role="user"
    )

    test_user.create()
    pass