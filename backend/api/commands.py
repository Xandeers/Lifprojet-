from flask.cli import with_appcontext
import click


@click.command("populate-products", help="Populate products table with Ciqual dataset")
@with_appcontext
def populate_products():
    print("hello")
