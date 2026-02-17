import json
import click
from flask.cli import with_appcontext
from models import db, User, Ship


@click.command(name='db-seed')
@with_appcontext
def db_seed():
    """Seeds the database based on the provided data.json file."""
    try:
        with open('data.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        click.echo("Error: 'data.json' file not found!")
        return

    # Seed users
    if User.query.first() is None:
        users_data = data.get('users', [])
        click.echo("Seeding users...")
        for user_data in users_data:
            new_user = User(name=user_data['name'])
            new_user.set_password(user_data['password'])
            db.session.add(new_user)
            click.echo(f"  - Added: {new_user.name}")
    else:
        click.echo("The 'users' table already contains data, skipping seed.")

    # Seed ships
    if Ship.query.first() is None:
        ships_data = data.get('ships', [])
        click.echo("Seeding ships...")
        for ship_data in ships_data:
            new_ship = Ship(
                affiliation=ship_data['affiliation'],
                category=ship_data['category'],
                crew=ship_data['crew'],
                length=ship_data['length'],
                manufacturer=ship_data['manufacturer'],
                model=ship_data['model'],
                roles=ship_data['roles'],
                ship_class=ship_data['ship_class']
            )
            db.session.add(new_ship)
            click.echo(f"  - Added: {new_ship.model}")
    else:
        click.echo("The 'ships' table already contains data, skipping seed.")

    db.session.commit()
    click.echo("Database seeding finished!")