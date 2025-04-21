export interface Product {
  id: number;
  name: string;
  category: "drink" | "cheese" | "fat" | "other";
  energy: number;
  proteins: number;
  sugars: number;
  saturated_fat: number;
  salt: number;
  fruits_veg: number;
  fibers: number;
  source: string;
  barcode: string | null;
}

export interface ProductSearchIngredient {
  quantity: number;
  unit: string;
  product: Product;
}
