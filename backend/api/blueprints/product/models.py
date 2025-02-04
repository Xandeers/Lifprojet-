from api import db 

# Product Industrial

# Product Model
class ProductIndustrial(db.Model):

    __tablename__ = 'products_industrials'

    # Fields

    barcode = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #--------macro liste--------
    carbohydrates= db.Column(db.Integer, nullable=False) # glucide
    energy = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False) #matiere grasse
    fiber = db.Column(db.Integer, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    salt = db.Column(db.Integer, nullable=False)
    saturated_fat = db.Column(db.Integer, nullable=False)
    fruits_vegetables_nuts_estimate  = db.Column(db.Integer, nullable=False)
    sugars = db.Column(db.Integer, nullable=False)
    sodium  = db.Column(db.Integer, nullable=False)
    #-------------------------
    nutriscore = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Date, default=datetime.utcnow().date)
    date_modified = db.Column(db.Date, default=datetime.utcnow().date)
    image = db.Column(db.String(255))


      def __init__(self, barcode, name, carbohydrates,energy, fat, fiber , proteins, salt, saturated_fat, fruits_vegetables_nuts_estimate, sugars, sodium,nutriscore , image):
      
          self.barcode = barcode
          self.name = name
          self.carbohydrates = carbohydrates
          self.energy = energy
          self.fat = fat
          self.fiber = fiber
          self.proteins = proteins 
          self.salt = salt
          self.saturated_fat = saturated_fat
          self.fruits_vegetables_nuts_estimate = fruits_vegetables_nuts_estimate
          self.sugars = sugars
          self.sodium = sodium 
          self.nutriscore = nutriscore
          self.image = image 
          

          # Methods to verify if product already exists
    @classmethod
    def is_product_taken(cls, barcode):
        """Vérifie si un produit existe deja"""
        return db.session.query(cls.barcode).filter_by(barcode=barcode).first() is not None

    