import click

from .extensions import db


def register_commands(app):
    @app.cli.command("seed")
    def seed():
        from .models import Item

        if not Item.query.first():
            db.session.add(Item(name="First item", description="Your API is ready."))
            db.session.commit()
            click.echo("Seeded sample item.")
        else:
            click.echo("Items already exist.")
