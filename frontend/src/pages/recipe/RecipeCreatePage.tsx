import { useState } from "react";
import Layout from "../../components/layout/Layout";
import { Product, ProductSearchIngredient } from "../../types/product";
import { useNavigate } from "react-router";
import { fetchAPI } from "../../utils/api";
import { Recipe } from "../../types/recipe";
import ProductSearch from "../../components/recipe/ProductSearch";
import Form from "../../components/forms/Form";
import { useAccount } from "../../hooks/useAccount";

interface IngredientInput extends ProductSearchIngredient {}

export default function RecipeCreatePage() {
  const { account } = useAccount();
  const [ingredients, setIngredients] = useState<IngredientInput[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const navigate = useNavigate();

  const handleAddProduct = (product: Product) => {
    const exists = selectedProducts.some((ing) => ing.id === product.id);
    if (!exists) {
      setSelectedProducts((prev) => [...prev, product]);
      setIngredients((prev) => [
        ...prev,
        { product, quantity: 100, unit: "g" },
      ]);
    }
  };

  const handleIngredientChange = (
    index: number,
    field: "quantity" | "unit",
    value: string | number
  ) => {
    const newIngredients = [...ingredients];
    if (field === "quantity") {
      newIngredients[index].quantity =
        typeof value === "number" ? value : Number(value);
    } else {
      newIngredients[index].unit = String(value);
    }
    setIngredients(newIngredients);
  };

  const handleRemoveProduct = (product: Product) => {
    setIngredients((prev) =>
      prev.filter((ing) => ing.product.id !== product.id)
    );
    setSelectedProducts((prev) => prev.filter((ing) => ing.id !== product.id));
  };

  const handleSubmit = async (formData: Record<string, FormDataEntryValue>) => {
    const { title, description, thumbnailUrl, instructions } = formData;
    const body = {
      title,
      description,
      thumbnail_url: thumbnailUrl,
      instructions,
      ingredients: ingredients.map((ing) => ({
        id: ing.product.id,
        quantity: ing.quantity,
        unit: ing.unit,
      })),
    };

    try {
      const created = await fetchAPI<Recipe>("POST", "/recipe/", body);
      navigate(`/recipe/${created.slug}`);
    } catch (err) {
      console.error("Erreur lors de la création :", err);
    }
  };

  const fields = [
    {
      name: "title",
      label: "Titre",
      type: "text",
      placeholder: "Titre de la recette",
    },
    {
      name: "description",
      label: "Description",
      type: "text",
      placeholder: "Description de la recette",
    },
    {
      name: "thumbnailUrl",
      label: "URL de l'image",
      type: "text",
      placeholder: "URL de l'image miniature",
    },
    {
      name: "instructions",
      label: "Instructions",
      type: "text",
      placeholder: "Instructions de préparation",
    },
  ];

  return (
    <Layout>
      <div className="max-w-2xl mx-auto space-y-4">
        <h1 className="text-2xl font-bold">Créer une recette</h1>
        <Form
          fields={fields}
          onSubmit={handleSubmit}
          submitText="Créer la recette"
        />
        <div className="space-y-2 mt-4">
          <h2 className="font-semibold">Ingrédients</h2>
          <ProductSearch
            onSelect={handleAddProduct}
            selectedProducts={selectedProducts}
            onRemove={handleRemoveProduct}
          />
          {ingredients.map((ing, index) => (
            <div key={ing.product.id} className="flex items-center gap-2">
              <span className="flex-1">{ing.product.name}</span>
              <input
                type="number"
                value={ing.quantity}
                onChange={(e) =>
                  handleIngredientChange(index, "quantity", e.target.value)
                }
                className="w-20 border p-1 rounded"
              />
              <input
                type="text"
                value={ing.unit}
                onChange={(e) =>
                  handleIngredientChange(index, "unit", e.target.value)
                }
                className="w-20 border p-1 rounded"
              />
              <button
                onClick={() => handleRemoveProduct(ing.product)}
                className="text-red-500 hover:text-red-700"
              >
                ❌
              </button>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
