import { useState } from "react";
import API from "../utils/api";

type ProgramData = {
  user_id: number;
  height_cm: number;
  weight_kg: number;
  age: number;
  gender: "male" | "female";
  activity_level: "sedentary" | "light" | "moderate" | "active" | "very_active";
  goal: "cutting" | "bulking" | "maintenance";
};

type Props = {
  userId: number;
  onSuccess: (program: any) => void;
};

export default function ProgramForm({ userId, onSuccess }: Props) {
  const [form, setForm] = useState<ProgramData>({
    user_id: userId,
    height_cm: 170,
    weight_kg: 65,
    age: 25,
    gender: "male",
    activity_level: "moderate",
    goal: "maintenance",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: name === "age" || name.includes("_cm") || name.includes("_kg") ? Number(value) : value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await API.post("/fitness_programs", form);
      onSuccess(res.data.program);
    } catch (err: any) {
      setError("Une erreur est survenue. Veuillez vérifier vos informations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <h2 className="text-xl font-semibold">Créer mon programme sportif</h2>

      <label>
        Taille (cm)
        <input type="number" name="height_cm" value={form.height_cm} onChange={handleChange} className="input" />
      </label>

      <label>
        Poids (kg)
        <input type="number" name="weight_kg" value={form.weight_kg} onChange={handleChange} className="input" />
      </label>

      <label>
        Âge
        <input type="number" name="age" value={form.age} onChange={handleChange} className="input" />
      </label>

      <label>
        Sexe
        <select name="gender" value={form.gender} onChange={handleChange} className="input">
          <option value="male">Homme</option>
          <option value="female">Femme</option>
        </select>
      </label>

      <label>
        Activité physique
        <select name="activity_level" value={form.activity_level} onChange={handleChange} className="input">
          <option value="sedentary">Sédentaire</option>
          <option value="light">Légère</option>
          <option value="moderate">Modérée</option>
          <option value="active">Active</option>
          <option value="very_active">Très active</option>
        </select>
      </label>

      <label>
        Objectif
        <select name="goal" value={form.goal} onChange={handleChange} className="input">
          <option value="cutting">Perte de poids</option>
          <option value="bulking">Prise de masse</option>
          <option value="maintenance">Maintien</option>
        </select>
      </label>

      {error && <p className="text-red-500">{error}</p>}

      <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded" disabled={loading}>
        {loading ? "Calcul..." : "Générer mon programme"}
      </button>
    </form>
  );
}
