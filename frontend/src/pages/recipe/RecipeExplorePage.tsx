import Layout from "../../components/layout/Layout.tsx";
import RecipeCard from "../../components/recipe/RecipeCard.tsx";
import { RecipeDifficulty } from "../../types/recipe.ts";

export default function RecipeExplorePage() {
  return (
    <Layout>
      <h1 className="font-bold text-3xl mb-3 pb-3 border-b-1 border-b-gray-300">
        Explorer de nouvelles recettes
      </h1>
      <div className="grid xl:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-3">
        <RecipeCard
          title="Couscous"
          image_url="https://www.rustica.fr/images/couscous-tajine-l790-h526.jpg.webp"
          description="c'est une pépite"
          prep_time={10}
          cook_time={30}
          difficulty={RecipeDifficulty.Hard}
          tags={["legume", "viande", "semoule", "cool", "bio"]}
          likes={20}
          published_at={Date.now().toLocaleString()}
          slug="couscous"
        />
        <RecipeCard
          title="Couscous"
          image_url="https://www.rustica.fr/images/couscous-tajine-l790-h526.jpg.webp"
          description="c'est une pépite"
          prep_time={10}
          cook_time={30}
          difficulty={RecipeDifficulty.Hard}
          tags={["legume", "viande", "semoule", "cool", "bio"]}
          likes={20}
          published_at={Date.now().toLocaleString()}
          slug="couscous"
        />
        <RecipeCard
          title="Couscous"
          image_url="https://www.rustica.fr/images/couscous-tajine-l790-h526.jpg.webp"
          description="c'est une pépite"
          prep_time={10}
          cook_time={30}
          difficulty={RecipeDifficulty.Hard}
          tags={["legume", "viande", "semoule", "cool", "bio"]}
          likes={20}
          published_at={Date.now().toLocaleString()}
          slug="couscous"
        />
      </div>
    </Layout>
  );
}
