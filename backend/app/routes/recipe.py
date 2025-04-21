from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Recipe
from app.schemas.recipe import RecipeCreate, RecipeBase
from app.services.recipe import RecipeService
from app.utils.session import get_current_user_id

router = APIRouter()

@router.get("/search")
def search_by_text(query: str, db: Session = Depends(get_db)) -> List[RecipeBase]:
    recipe_service = RecipeService(db)
    results = recipe_service.search_recipes_fts(query)
    recipes = [RecipeBase.model_validate(recipe) for recipe in results]
    return recipes

# WIP: Le feed est clairement améliorable
@router.get("/feed")
def feed(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return (db
            .query(Recipe)
            .order_by(desc(Recipe.updated_at))
            .offset(offset)
            .limit(limit)
            .all())

@router.post("/")
def create(recipe_data: RecipeCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)) -> RecipeBase:
    recipe_service = RecipeService(db)
    try:
        recipe = recipe_service.create_recipe(recipe_data, current_user_id)
        new_recipe = recipe_service.get_recipe(recipe.slug)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_recipe #type: ignore

@router.get("/{slug}")
def info(slug: str, db: Session = Depends(get_db)) -> RecipeBase:
    recipe_service = RecipeService(db)
    try:
        recipe = recipe_service.get_recipe(slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return recipe #type: ignore

@router.put("/{slug}")
def modify(slug: str, recipe_data: RecipeCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)) -> RecipeBase:
    recipe_service = RecipeService(db)
    try:
        recipe = recipe_service.modify_recipe(slug, recipe_data, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return recipe #type: ignore

@router.delete("/{slug}")
def delete(slug: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    recipe_service = RecipeService(db)
    try:
        recipe_service.delete_recipe(slug, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return HTTPException(status_code=200, detail="Recipe deleted successfully")

@router.put("/{slug}/like")
def like(slug: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    recipe_service = RecipeService(db)
    try:
        liked = recipe_service.like_recipe(slug, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"liked": liked}

@router.get("/{slug}/like")
def like(slug: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    recipe_service = RecipeService(db)
    try:
        liked = recipe_service.get_like_recipe_status(slug, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"liked": liked}