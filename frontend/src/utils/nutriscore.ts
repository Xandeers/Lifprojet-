export function nutriscore_to_grade(score: number) {
  if (score <= -1) return "A";
  if (score <= 2) return "B";
  if (score <= 10) return "C";
  if (score <= 18) return "D";
  else return "E";
}
