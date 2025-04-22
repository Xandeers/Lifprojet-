import { useEffect, useState } from "react";
import { Product } from "../../types/product";
import { fetchAPI } from "../../utils/api";

interface ProductSearchProps {
  onSelect: (product: Product) => void;
  selectedProducts: Product[];
  onRemove: (product: Product) => void;
}

export default function ProductSearch({
  onSelect,
  selectedProducts,
  onRemove,
}: ProductSearchProps) {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

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

  useEffect(() => {
    if (searchTerm.length < 3) {
      setResults([]);
      return;
    }

    const timer = setTimeout(() => {
      searchProducts(searchTerm);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSelectProduct = (product: Product) => {
    if (!selectedProducts.some((p) => p.id === product.id)) {
      onSelect(product);
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

      <ul> {/* si ul vide peut être afficher "Pas de résultat" */}
        {results.map((product) => (
          <li
            key={product.id}
            className="flex justify-between items-center cursor-pointer hover:bg-gray-100 p-3 border-1 border-gray-300"
            onClick={() => handleSelectProduct(product)}
          >
            <span>{product.name}</span>
            {selectedProducts.some((p) => p.id === product.id) && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onRemove(product);
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
