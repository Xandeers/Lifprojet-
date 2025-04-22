import { Link, useParams } from "react-router";
import Layout from "../../components/layout/Layout.tsx";
import { Recipe } from "../../types/recipe";
import { useEffect, useState } from "react";
import { fetchAPI } from "../../utils/api";
import { nutriscore_to_grade } from "../../utils/nutriscore";

export default function RecipePage() {
  const { slug } = useParams<{ slug: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const data = await fetchAPI<Recipe>("GET", `/recipe/${slug}`);
        setRecipe(data);
      } catch (error) {
        console.error("Erreur lors de la récupération de la recette:", error);
      }
    };

    if (slug) {
      fetchRecipe();
    }
  }, [slug]);

  if (!recipe) {
    return (
      <Layout>
        <div>Chargement...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="recipe-detail-container">
        <h1 className="text-3xl font-bold">{recipe.title}</h1>
        <img src={`http://127.0.0.1:8000/upload/thumbnail/${recipe.thumbnail_url}`} alt={recipe.title} className="w-full h-60 object-cover mt-4 rounded-lg" />
        <p className="text-sm text-gray-500 mt-2">Publié le {new Date(recipe.created_at).toLocaleDateString()} par <Link to={`/users/${recipe.author.username}`}><b>{recipe.author.username}</b></Link></p>

        <div className="mt-4">
          <h3 className="text-xl font-semibold">Description:</h3>
          <p>{recipe.description}</p>
        </div>

        <div className="mt-4">
        <h3 className="text-xl font-semibold">Nutriscore:</h3>
          <p>{nutriscore_to_grade(recipe.nutriscore)}</p>
        </div>

        <div className="mt-4">
          <h3 className="text-xl font-semibold">Ingrédients:</h3>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>
                {ingredient.quantity} {ingredient.unit} de {ingredient.product.name} ({ingredient.product.category})
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-4">
          <h3 className="text-xl font-semibold">Instructions:</h3>
          <p>{recipe.instructions}</p>
        </div>

        <div className="mt-4">
          <p className="text-sm text-gray-600">Likes: {recipe.likes_count}</p>
        </div>
      </div>
    </Layout>
  );
}
