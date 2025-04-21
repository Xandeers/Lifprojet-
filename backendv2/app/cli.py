import typer
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from typing_extensions import Annotated

from app.database import get_session
from app.models import Product, ProductCategory
import pandas as pd
import os
import json
import requests

load_dotenv()

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

############################# FAKE RECIPES #############################

@cli.command()
def fake_recipes(number: Annotated[int, typer.Argument()], default_thumbnail: Annotated[str, typer.Argument()] = ""):
    print("Generating fakes recipes with OpenAI as AI Wrapper")

    # openai connection
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    # api connection
    BASE_URL = "http://127.0.0.1:8000"
    login_data = {
        "email": "faker@faker.com",
        "password": "faker"
    }

    session = requests.session()
    login_res = session.post(f"{BASE_URL}/auth/login", json=login_data)
    if login_res.status_code != 200:
        print("Unable to login to API")
        exit()

    # prompt pour une recette
    prompt = """
    Tu es un générateur de recette. Tu dois répondre uniquement en JSON, sans aucun texte avant ou après.

    Voici le format JSON exact à respecter :
    {
      "title": "string",
      "description": "string",
      "thumbnail_url": "string",
      "instructions": "string",
      "ingredients": [
        {
          "id": 0,
          "quantity": 0
        }
      ]
    }

    Consignes :
    - Les champs id et quantity doivent être des entiers entre 1 et 100.
    - Limite-toi à exactement 3 ingrédients.
    - Tous les champs doivent être présents.
    - Ne retourne rien d’autre que l’objet JSON.
    """

    for i in range (0, number):
        response = client.responses.create(
            model="gpt-3.5-turbo",
            input=prompt
        )

        output = response.output_text
        try:
            recipe_data = json.loads(output)
            recipe_data["thumbnail_url"] = default_thumbnail
            post_response = session.post(f"{BASE_URL}/recipe", json=recipe_data)
            if post_response.status_code == 200:
                print(f"✅ Recette {recipe_data["title"]} crée")
            else:
                print("❌: Erreur : ", post_response.status_code, post_response.text)
        except json.JSONDecodeError as e:
            print("❌: Erreur de parsing JSON :", e)


if __name__ == "__main__":
    cli()