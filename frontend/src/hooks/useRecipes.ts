import { useEffect, useState, useRef, useCallback } from "react";
import { Recipe } from "../types/recipe";
import { fetchAPI } from "../utils/api";

export default function useRecipes(limit = 10) {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const loaderRef = useRef(null);

  const fetchRecipes = useCallback(async () => {
    if (loading || !hasMore) return;
    setLoading(true);
    try {
      const data = await fetchAPI<Recipe[]>(
        "GET",
        `/recipe/feed?offset=${offset}&limit=${limit}`
      );
      if (data.length < limit) setHasMore(false);
      setRecipes((prev) => [...prev, ...data]);
      setOffset((prev) => prev + limit);
    } catch (err) {
      console.error("Erreur chargement recettes :", err);
    } finally {
      setLoading(false);
    }
  }, [offset, hasMore, loading, limit]);

  useEffect(() => {
    fetchRecipes();
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore) {
          fetchRecipes();
        }
      },
      { threshold: 1 }
    );
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => {
      if (loaderRef.current) observer.unobserve(loaderRef.current);
    };
  }, [fetchRecipes, hasMore]);

  return { recipes, loaderRef };
}
