import { Account } from "../hooks/useAuth";

export enum RecipeDifficulty {
  Beginner = 1,
  Intermediate = 2,
  Hard = 3,
}

export type Recipe = {
  id: number;
  title: string;
  description: string;
  slug: string;
  thumbnail_url: string;
  instructions: string;
  nutriscore: number;
  ingredients: {
    quantity: number;
    unit: string;
    product: {
      name: string;
      category: string;
    };
  }[];
  likes_count: number;
  created_at: string;
  updated_at: string;
  author: Account;
};
