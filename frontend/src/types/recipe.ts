export enum RecipeDifficulty {
  Beginner = 1,
  Intermediate = 2,
  Hard = 3,
}

export type Recipe = {
  title: string;
  slug: string;
  content?: string;
  image_url: string;
  description: string;
  prep_time: number;
  cook_time: number;
  difficulty: RecipeDifficulty;
  tags: String[];
  likes: number;
  published_at: string;
};
