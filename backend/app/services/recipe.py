from sqlalchemy import select, text, func
from sqlalchemy.orm import Session, selectinload

from app.models import Recipe, Product, RecipeIngredient, RecipeLike
from app.schemas.recipe import RecipeCreate, RecipeBase


class RecipeService:
    def __init__(self, db: Session):
        self.db = db

    def is_recipe_exists(self, title: str) -> bool:
        return self.db.execute(select(Recipe).where(Recipe.title == title)).first() is not None

    def get_recipe(self, slug: str) -> RecipeBase:
        recipe = (
            self.db.query(Recipe)
            .options(
                selectinload(Recipe.ingredients).selectinload(RecipeIngredient.product),
                selectinload(Recipe.author)
            )
            .filter(Recipe.slug == slug)
            .first()
        )
        if recipe is None:
            raise ValueError(f"Recipe {slug} not found")

        likes_count = self.db.query(func.count(RecipeLike.recipe_id)).filter(RecipeLike.recipe_id == recipe.id).scalar()

        validated = RecipeBase.model_validate(recipe)
        return validated.model_copy(update={"likes_count": likes_count})

    def create_recipe(self, recipe_data: RecipeCreate, author_id: int) -> Recipe:
        # if self.is_recipe_exists(recipe_data.title):
        #    raise ValueError(f'Recipe [{recipe_data.title}] already exists')

        recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            thumbnail_url=recipe_data.thumbnail_url,
            instructions=recipe_data.instructions,
            author_id=author_id
        )

        for ingredient_data in recipe_data.ingredients:

            product = self.db.query(Product).filter(Product.id == ingredient_data.id).first()
            if not product:
                raise ValueError(f"The product number {ingredient_data.id} doesn't exist.")

            ingredient = RecipeIngredient(
                quantity=ingredient_data.quantity,
                unit=ingredient_data.unit
            )
            ingredient.product = product
            ingredient.recipe = recipe
            recipe.ingredients.append(ingredient)

        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)

        return recipe

    def modify_recipe(self, slug: str, recipe_data: RecipeCreate, author_id: int) -> Recipe:
        # check if recipe exists
        recipe = self.db.query(Recipe).filter(Recipe.slug == slug).first()
        if not recipe:
            raise ValueError(f"Recipe [{slug}] not found")

        # check if recipe owner
        if recipe.author.id != author_id:
            raise ValueError(f"You are not the owner of this recipe")

        # update fields
        recipe.title = recipe_data.title
        recipe.description = recipe_data.description
        recipe.thumbnail_url = recipe_data.thumbnail_url
        recipe.instructions = recipe_data.instructions

        # clear old ingredients (total replace)
        recipe.ingredients.clear()
        self.db.query(RecipeIngredient).filter((RecipeIngredient.recipe_id == recipe.id)).delete()

        # add new ingredients
        for ingredient_data in recipe_data.ingredients:
            product = self.db.query(Product).filter(Product.id == ingredient_data.id).first()
            if not product:
                raise ValueError(f"The product number {ingredient_data.id} doesn't exist.")

            ingredient = RecipeIngredient(
                quantity=ingredient_data.quantity,
                unit=ingredient_data.unit,
            )
            ingredient.product = product
            ingredient.recipe = recipe
            self.db.add(ingredient)

            recipe.ingredients.append(ingredient)

        # commit changes
        self.db.commit()
        self.db.refresh(recipe)

        return recipe #type: ignore

    def delete_recipe(self, slug: str, author_id: int) -> bool:
        recipe = self.db.query(Recipe).filter(Recipe.slug == slug).first()

        # check if exists
        if not recipe:
            raise ValueError(f"Recipe [{slug}] not found")

        # check if owner
        if recipe.author_id != author_id:
            raise ValueError(f"You are not the owner of this recipe")

        # delete
        self.db.delete(recipe)
        self.db.commit()

    def search_recipes_fts(self, query: str):
        sql = text("""
                       SELECT 
                           *,
                           ts_rank(search_field, websearch_to_tsquery('french', :query)) AS rank
                       FROM recipes
                       WHERE search_field @@ websearch_to_tsquery('french', :query)
                       ORDER BY rank DESC
                       LIMIT 15
                   """)
        ids = [row[0] for row in self.db.execute(sql, {"query": query}).fetchall()]
        recipes = self.db.query(Recipe).filter(Recipe.id.in_(ids)).all()
        return recipes

    def like_recipe(self, slug: str, user_id: int) -> bool:
        # check if recipe exists
        recipe = self.db.query(Recipe).filter(Recipe.slug == slug).first()
        if not recipe:
            raise ValueError(f"Recipe [{slug}] not found")

        # check if already liked
        existing_like = self.get_like_recipe(slug, user_id)

        # unlike
        if existing_like:
            self.db.delete(existing_like)
            self.db.commit()
            return False

        # like
        new_like = RecipeLike(user_id=user_id, recipe_id=recipe.id)
        self.db.add(new_like)
        self.db.commit()

        return True

    def get_like_recipe(self, slug: str, user_id: int):
        # check if recipe exists
        recipe = self.db.query(Recipe).filter(Recipe.slug == slug).first()
        if not recipe:
            raise ValueError(f"Recipe [{slug}] not found")

        # check if already liked
        existing_like = self.db.query(RecipeLike).filter_by(user_id=user_id, recipe_id=recipe.id).first()
        return existing_like

    def get_like_recipe_status(self, slug: str, user_id: int):
        existing_like = self.get_like_recipe(slug, user_id)
        if existing_like:
            return True
        return False