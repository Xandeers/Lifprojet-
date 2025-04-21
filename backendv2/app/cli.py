import typer
from pathlib import Path
from app.database import get_session
from app.models import Product, ProductCategory
import pandas as pd

cli = typer.Typer()

def resolve_category(code):
    if code == "06":
        return ProductCategory.drink
    elif code == "05":
        return ProductCategory.cheese
    elif code == "09":
        return ProductCategory.fat
    else:
        return ProductCategory.other

def parse_value(value):
    if value == "-" or not value:
        return 0
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return 0

@cli.command()
def import_ciqual():
    print("Importing from CIQUAL")

    filepath = Path("data/ciqual_2020.xls")
    df = pd.read_excel(filepath, dtype=str).fillna("")  # open xls file with Pandas

    # groups codes
    grp_codes = ["02", "03", "04", "05", "06", "09"]

    # db instance
    db = get_session()

    # populate
    added = -1  # count number of row added
    for _, row in df.iterrows():
        if row["alim_grp_code"] not in grp_codes:
            continue
        try:
            with get_session() as db:
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
                    fruits_veg=0,  # pas dispo dans Ciqual
                    fibers=fibers,
                    source="ciqual",
                )
                db.add(product)
                db.commit()
                added += 1
        except Exception as e:
            print(f"Error at line: {row.get('alim_nom_fr', '?')} - {e}")

if __name__ == "__main__":
    cli()