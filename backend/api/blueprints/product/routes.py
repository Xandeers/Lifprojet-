from flask import Blueprint, request, jsonify
from api import db
from .models import ProductIndustrial 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import requests

product_bp = Blueprint('product', __name__)

#recupere tout les produits 

@product_bp.route('/industrial/all', methods=['GET'])
def get_all_products():
    # Récupérer le paramètre 'page' depuis l'URL (page=2, par défaut page=1)
    page = request.args.get('page', default=1, type=int)  # Page par défaut = 1 si non précisé
    per_page = 20 # Nombre de produits par page

    #récupérer les produits industriels avec pagination
    products = ProductIndustrial.query.paginate(page=page, per_page=per_page,error_out=False)

    # Sérialiser les produits
    result = []
    for product in products.items:
        result.append({
            'barcode': product.barcode,
            'name': product.name,
            'carbohydrates': product.carbohydrates,
            'energy': product.energy,
            'fat': product.fat,
            'fiber': product.fiber,
            'proteins': product.proteins,
            'salt': product.salt,
            'saturated_fat': product.saturated_fat,
            'fruits_vegetables_nuts_estimate': product.fruits_vegetables_nuts_estimate,
            'sugars': product.sugars,
            'sodium': product.sodium,
            'nutriscore': product.nutriscore,
            'image': product.image,
            'information': product.information,
        })
    # Retourner les produits sous forme de JSON avec les informations de pagination
    return jsonify({
        'products': result,
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    })

    
#recupere tout les produit qui on un nutriscore qui a été prealablement choisi 

@product_bp.route('/industrial/nutriscore-<letter>', methods=['GET'])
def get_products_nutriscore_x(letter):

    #verification du nutriscore et retourne une erreur en cas de recherche non correct
    check_nutriscore = ['A','B','C','D','E']
    if letter not in check_nutriscore:
        return jsonify({'error':'Invalid nutriscore letter' }), 400

    # Récupérer le paramètre 'page' depuis l'URL (page=2, par défaut page=1)
    page = request.args.get('page', default=1, type=int)  # Page par défaut = 1 si non précisé
    per_page = 20 # Nombre de produits par page

    try:
        #récupérer les produits industriels avec pagination
        products = ProductIndustrial.query.filter(ProductIndustrial.nutriscore == letter).paginate(page=page, per_page=per_page,error_out = False)

        if not products.items:
            return jsonify({'error': 'No products found for this nutriscore'}), 404
        # Sérialiser les produits
        result = []
        for product in products.items:
            result.append({
                'barcode': product.barcode,
                'name': product.name,
                'carbohydrates': product.carbohydrates,
                'energy': product.energy,
                'fat': product.fat,
                'fiber': product.fiber,
                'proteins': product.proteins,
                'salt': product.salt,
                'saturated_fat': product.saturated_fat,
                'fruits_vegetables_nuts_estimate': product.fruits_vegetables_nuts_estimate,
                'sugars': product.sugars,
                'sodium': product.sodium,
                'nutriscore': product.nutriscore,
                'image': product.image,
                    'information': product.information,
            })

        # Retourner les produits sous forme de JSON avec les informations de pagination
        return jsonify({
            'products': result,
            'total': products.total,
            'pages': products.pages,
            'current_page': products.page   
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/industrial/<name>', methods=['GET'])
def search_product_by_name(name):
    # Récupérer le paramètre 'page' depuis l'URL (page=2, par défaut page=1)
    page = request.args.get('page', default=1, type=int)  # Page par défaut = 1 si non précisé
    per_page = 20  # Nombre de produits par page
    try:
        # Utiliser la fonction pg_trgm pour une recherche floue sur le nom
        products = ProductIndustrial.query.filter(
            db.func.similarity(db.cast(ProductIndustrial.name, db.String), name) > 0.3  # Ajuster le seuil selon tes besoins
        ).paginate(page=page, per_page=per_page, error_out=False)

        # Sérialiser les produits
        result = []
        for product in products.items:
            result.append({
                'barcode': product.barcode,
                'name': product.name,
                'carbohydrates': product.carbohydrates,
                'energy': product.energy,
                'fat': product.fat,
                'fiber': product.fiber,
                'proteins': product.proteins,
                'salt': product.salt,
                'saturated_fat': product.saturated_fat,
                'fruits_vegetables_nuts_estimate': product.fruits_vegetables_nuts_estimate,
                'sugars': product.sugars,
                'sodium': product.sodium,
                'nutriscore': product.nutriscore,
                'image': product.image,
                'information': product.information,
            })
    
        # Retourner les produits sous forme de JSON avec les informations de pagination
        return jsonify({
            'products': result,
            'total': products.total,
            'pages': products.pages,
            'current_page': products.page
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/industrial/get_product/<barcode>', methods=['GET'])
def add_product(barcode):
    try:
        #Appel de l'api pour recuperer un produit avec un nom specifique 
        url = f'https://world.openfoodfacts.org/api/v3/product/{barcode}.json'

        #faire la requete pour recuperer le produit
        response = requests.get(url)

        if response.status_code !=200:
            return jsonify({'error': 'Product not found or failed to fetch'}), 404

        #recuperation des donner du produit sous forme de JSON
        product_data = response.json()
        print(product_data)

        #verification si les donner existent
        if 'product' not in product_data:
            return jsonify({'error': 'product details not found'}), 404

        product = product_data['product']
        nutriments = product['nutriments']

        #extraire les information

        print(product)

        name = product.get('product_name', 'N/A')
        barcode = product.get('code', 'N/A')
        carbohydrates =float(nutriments.get('carbohydrates_100g', 0))
        energy = float(nutriments.get('energy_value',0))
        fat = float(nutriments.get('fat_100g', 0))
        fiber = float(nutriments.get('fiber_100g', 0))
        proteins = float(nutriments.get('proteins_100g',0))
        salt = float(nutriments.get('salt_100g', 0))
        saturated_fat = float(nutriments.get('saturated-fat_100g', 0))
        fruits_vegetables_nuts_estimate = float(nutriments.get('fruits_vegetables_nuts_estimate', 0))
        sugars = float(nutriments.get('sugars_100g', 0))
        sodium = float(nutriments.get('sodium_100g', 0))
        nutriscore = product.get('nutriscore_grade', 'N/A')
        image = product.get('image_url', '')
        information = product.get('ingredients_text', '')


        #ajout du produit dans la bd que si il n'y est pas 
        existing_product=ProductIndustrial.query.filter_by(barcode=barcode).first()

        if not existing_product:
            new_product = ProductIndustrial(
                barcode=barcode,
                name=name,
                carbohydrates=carbohydrates,
                energy=energy,
                fat=fat,
                fiber=fiber,
                proteins=proteins,
                salt=salt,
                saturated_fat=saturated_fat,
                fruits_vegetables_nuts_estimate=fruits_vegetables_nuts_estimate,
                sugars=sugars,
                sodium=sodium,
                nutriscore=nutriscore,
                image=image,
                information=information
            )
            db.session.add(new_product)
            db.session.commit()
            message = 'product added to the databaase.'
        else:
            message = 'product already exists in the database.'

        #retourne les information du produit 
        return jsonify({
            'message': message,
            'name': name,
            'barcode': barcode,
            'energy': energy,
            'fat': fat,
            'protein': proteins,
            'nutriscore': nutriscore
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
