from flask import Blueprint, request, jsonify
from api import db
from models import ProductIndustrial 


# Créer le Blueprint
product_bp = Blueprint('product', __name__)

#recupere tout les produits 

@product_bp.route('/product/industrial/all', methods=['GET'])
def get_all_products():
    # Récupérer le paramètre 'page' depuis l'URL (page=2, par défaut page=1)
    page = request.args.get('page', default=1, type=int)  # Page par défaut = 1 si non précisé
    per_page = 20 # Nombre de produits par page

    #récupérer les produits industriels avec pagination
    products = ProductIndustrial.query.paginate(page, per_page, False)

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

    @product_bp.route('/product/industrial/nutriscore-<letter>', methods=['GET'])
def get_products_nutriscore_x(letter):
    # Récupérer le paramètre 'page' depuis l'URL (page=2, par défaut page=1)
    page = request.args.get('page', default=1, type=int)  # Page par défaut = 1 si non précisé
    per_page = 20 # Nombre de produits par page

    #récupérer les produits industriels avec pagination
    products = ProductIndustrial.query.filter_by(nutriscore='letter')\
                                      .paginate(page, per_page, False)

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

