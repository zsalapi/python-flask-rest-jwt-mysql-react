import json
import click
from flask.cli import with_appcontext
from models import db, User, Ship


@click.command(name='db-seed')
@with_appcontext
def db_seed():
    """A megadott data.json fájl alapján feltölti az adatbázist."""
    try:
        with open('data.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        click.echo("Hiba: a 'data.json' fájl nem található!")
        return

    # Felhasználók feltöltése
    if User.query.first() is None:
        users_data = data.get('users', [])
        click.echo("Felhasználók feltöltése...")
        for user_data in users_data:
            new_user = User(name=user_data['name'])
            new_user.set_password(user_data['password'])
            db.session.add(new_user)
            click.echo(f"  - Hozzáadva: {new_user.name}")
    else:
        click.echo("A 'users' tábla már tartalmaz adatokat, a feltöltés kihagyva.")

    # Hajók feltöltése
    if Ship.query.first() is None:
        ships_data = data.get('ships', [])
        click.echo("Hajók feltöltése...")
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
            click.echo(f"  - Hozzáadva: {new_ship.model}")
    else:
        click.echo("A 'ships' tábla már tartalmaz adatokat, a feltöltés kihagyva.")

    db.session.commit()
    click.echo("Adatbázis feltöltése befejeződött!")