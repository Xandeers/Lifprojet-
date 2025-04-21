import Layout from "../../components/layout/Layout.tsx";
import RecipeCard from "../../components/recipe/RecipeCard";
import useRecipes from "../../hooks/useRecipes";

export default function RecipeExplorePage() {
  const { recipes, loaderRef } = useRecipes();

  return (
    <Layout>
      <h1 className="font-bold text-3xl mb-3 pb-3 border-b border-gray-300">
        Explorer de nouvelles recettes
      </h1>
      <div className="flex flex-col gap-4">
        {recipes.map((recipe) => (
          <RecipeCard
            key={recipe.id}
            {...{
              ...recipe,
            }}
          />
        ))}
        <div ref={loaderRef} className="py-10 text-center text-gray-400">
          Chargement...
        </div>
      </div>
    </Layout>
  );
}
