from api import db, ma
from api.models.user import User
from api.schemas.user import UserSchema

# 🔹 Modèle Recipe (ajout de la relation avec User)
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_public = db.Column(db.Boolean, default=True)
    nutriscore = db.Column(db.String(1), nullable=False)

    # 🔗 Ajout de la clé étrangère vers User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, tag, content, nutriscore, user_id, is_public=True):
        self.title = title
        self.tag = tag
        self.content = content
        self.nutriscore = nutriscore
        self.is_public = is_public
        self.user_id = user_id

    def add_like(self):
        self.likes += 1
        db.session.commit()

# 🔹 Schéma Recipe (ajout de l'auteur)
class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    tag = ma.auto_field()
    content = ma.auto_field()
    likes = ma.auto_field()
    created_at = ma.auto_field()
    is_public = ma.auto_field()
    nutriscore = ma.auto_field()
    user_id = ma.auto_field()
    author = ma.Nested(UserSchema, only=("id", "username"))  # Infos minimales sur l'auteur

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)