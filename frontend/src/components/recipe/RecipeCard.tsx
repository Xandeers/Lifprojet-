import { useState, useEffect } from "react";
import { Link } from "react-router";
import { Recipe } from "../../types/recipe.ts";
import { Heart } from "lucide-react";
import { fetchAPI } from "../../utils/api";
import { useToasts } from "../../contexts/ToastContext";

export default function RecipeCard(data: Recipe) {
  const [liked, setLiked] = useState(false);
  const { pushToast } = useToasts();

  useEffect(() => {
    const fetchLikeStatus = async () => {
      try {
        const response = await fetchAPI<{ liked: boolean }>(
          "GET",
          `/recipe/${data.slug}/like`
        );
        setLiked(response.liked);
      } catch (error) {
        console.error("Erreur lors de la récupération du statut du like:", error);
      }
    };

    fetchLikeStatus();
  }, [data.slug]);

  const handleLikeToggle = async () => {
    try {
      const response = await fetchAPI<{ liked: boolean }>(
        "PUT",
        `/recipe/${data.slug}/like`
      );
      setLiked(response.liked);
      if (response.liked)
        pushToast({
          content: `Vous avez liké la recette ${data.title}`,
          type: "success",
          duration: 0.5
        });
      else
        pushToast({
          content: `Vous avez unlike la recette ${data.title}`,
          type: "danger",
          duration: 0.5
        });
    } catch (error) {
      console.error("Erreur lors du clic sur like/unlike:", error);
    }
  };

  return (
    <div className="border border-gray-200 shadow-xs rounded-lg overflow-hidden w-full hover:shadow-md duration-150">
      <div className="flex items-stretch">
        <Link to={`/recipe/${data.slug}`}>
          <img
            src={data.thumbnail_url}
            alt="recipe image"
            className="w-32 h-32 object-cover brightness-90 hover:brightness-100 flex-shrink-0"
          />
        </Link>

        <div className="p-4 flex flex-col justify-between flex-grow">
          <Link to={`/recipe/${data.slug}`}>
            <h3 className="text-lg font-semibold truncate">{data.title}</h3>
            <p className="text-gray-600 text-sm mt-1 line-clamp-2">{data.description}</p>
          </Link>
        </div>

        <div className="p-10 flex items-start self-center">
          <button
            className={`transition ${liked ? "text-pink-500" : "text-gray-400"} hover:text-pink-600`}
            onClick={handleLikeToggle}
            aria-label="Like recipe"
          >
            <Heart size={30} fill={liked ? "#ec4899" : "none"} />
          </button>
        </div>
      </div>
    </div>
  );
}
