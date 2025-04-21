import { useEffect, useState } from "react";
import { Product } from "../../types/product";
import { fetchAPI } from "../../utils/api";
interface ProductSearchProps {
  onSelect: (product: Product) => void;
  selectedProducts: Product[]; // Liste des produits déjà sélectionnés
  onRemove: (product: Product) => void; // Fonction pour supprimer un produit de la sélection
}

interface ProductSearchProps {
  onSelect: (product: Product) => void;
  selectedProducts: Product[]; // Liste des produits déjà sélectionnés
  onRemove: (product: Product) => void; // Fonction pour supprimer un produit de la sélection
}

export default function ProductSearch({
  onSelect,
  selectedProducts,
  onRemove,
}: ProductSearchProps) {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // Fonction pour effectuer la recherche dans l'API
  const searchProducts = async (query: string) => {
    setLoading(true);
    try {
      const products = await fetchAPI<Product[]>(
        "GET",
        `/product/search?query=${query}`
      );
      setResults(products);
    } catch (error) {
      console.error("Erreur lors de la recherche des produits", error);
    }
    setLoading(false);
  };

  // Déclenche la recherche dès qu'une lettre est tapée (debouncing)
  useEffect(() => {
    if (searchTerm.length < 3) {
      setResults([]); // Si la recherche est trop courte, on vide les résultats
      return;
    }

    const timer = setTimeout(() => {
      searchProducts(searchTerm);
    }, 300); // 300ms de délai avant de lancer la requête (debouncing)

    return () => clearTimeout(timer); // Nettoie le timer au changement de terme de recherche
  }, [searchTerm]);

  // Fonction pour gérer la sélection d'un produit
  const handleSelectProduct = (product: Product) => {
    if (!selectedProducts.some((p) => p.id === product.id)) {
      onSelect(product); // Ajoute le produit à la sélection si ce n'est pas déjà le cas
    }
  };

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Rechercher un produit"
        className="w-full border p-2 rounded"
      />

      {loading && <p>Chargement...</p>}

      <ul>
        {results.map((product) => (
          <li
            key={product.id}
            className="flex justify-between items-center cursor-pointer hover:bg-gray-100 p-2 border-1 border-gray-300 p-3"
            onClick={() => handleSelectProduct(product)} // Sélectionne le produit
          >
            <span>{product.name}</span>
            {selectedProducts.some((p) => p.id === product.id) && (
              <button
                onClick={(e) => {
                  e.stopPropagation(); // Empêche la sélection du produit lors du clic sur la croix
                  onRemove(product); // Appelle la fonction pour supprimer le produit
                }}
                className="text-red-500 hover:text-red-700 ml-2"
              >
                ❌
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
