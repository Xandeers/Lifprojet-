import { Link } from "react-router";
import { Recipe } from "../../types/recipe.ts";

export default function RecipeCard(data: Recipe) {
  return (
    <div className="border border-gray-200 shadow-xs rounded-lg overflow-hidden w-80 sm:w-full hover:shadow-md duration-150">
      <Link to={`/recipe/${data.slug}`}>
        <img
          src={data.image_url}
          alt="recipe image"
          className="w-full h-40 object-cover brightness-90 hover:brightness-100"
        />
      </Link>
      <div className="p-4">
        <h3 className="text-xl font-semibold truncate">{data.title}</h3>
        <p className="text-gray-600 text-sm mt-1">{data.description}</p>
        <div className="mt-2 flex flex-wrap space-x-2 items-center">
          {data.tags.slice(0, 4).map((tag, key) => (
            <span
              key={key}
              className="bg-blue-100 text-blue-800 text-xs font-semibold py-1 px-2 rounded-full"
            >
              {tag}
            </span>
          ))}
          {data.tags.length > 4 && (
            <span className="text-blue-800 text-xs font-semibold">
              +{data.tags.length - 4}
            </span>
          )}
        </div>
        <div>
          <p className="mt-3 text-sm text-gray-500">
            Préparation: {data.prep_time} min | Cuisson: {data.cook_time} min
          </p>
          <div className="flex items-center text-sm gap-2">
            Difficulté:{" "}
            {Array.from({ length: data.difficulty }, (_, key) => (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="size-4"
                key={key}
              >
                <path
                  fillRule="evenodd"
                  d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z"
                  clipRule="evenodd"
                />
              </svg>
            ))}
            |<p>Likes: {data.likes}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
