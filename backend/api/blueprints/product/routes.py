from flask import request, jsonify
from api import db
from .models import ProductIndustrial 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from . import product_bp

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

