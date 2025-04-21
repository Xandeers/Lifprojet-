from flask.cli import with_appcontext
import click
import pandas as pd
from api.extensions import db
from api.models.product import Product
from pathlib import Path


def resolve_category(code):
    if code == "06":
        return "drink"
    elif code == "05":
        return "cheese"
    elif code == "09":
        return "fat"
    else:
        return "other"


def parse_value(value):
    if value == "-" or not value:
        return -1
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return -1


@click.command("import-ciqual", help="Populate products table with Ciqual dataset")
@with_appcontext
def import_ciqual():
    print("Populate products table with Ciqual Dataset...")
    click.echo(f"Reading Ciqual 2020 dataset")
    filepath = Path("data/ciqual_2020.xls")

    df = pd.read_excel(filepath, dtype=str).fillna("")  # open xls file with Pandas
    # groups codes
    grp_codes = ["02", "03", "04", "05", "06", "09"]

    # populate
    added = -1  # count number of row added
    for _, row in df.iterrows():
        if row["alim_grp_code"] not in grp_codes:
            continue
        try:
            print(f"Processing {row["alim_nom_fr"]}")

            # map values
            energy = parse_value(row["Energie, Règlement UE N° 1169/2011 (kcal/100 g)"])
            proteins = parse_value(row["Protéines, N x facteur de Jones (g/100 g)"])
            sugars = parse_value(row["Sucres (g/100 g)"])
            saturated_fat = parse_value(row["AG saturés (g/100 g)"])
            salt = parse_value(row["Sel chlorure de sodium (g/100 g)"])
            fibers = parse_value(row["Fibres alimentaires (g/100 g)"])

            # add to database
            product = Product(
                name=row["alim_nom_fr"],
                category=resolve_category(row["alim_grp_code"]),
                energy=energy,
                proteins=proteins,
                sugars=sugars,
                saturated_fat=saturated_fat,
                salt=salt,
                fruits_veg=-1,  # pas dispo dans Ciqual
                fibers=fibers,
                source="ciqual",
            )
            db.session.add(product)
            db.session.commit()
            added += 1
        except Exception as e:
            click.echo(f"Error at line: {row.get('alim_nom_fr', '?')} - {e}")

    print(f"{added} products added to database")
