import { useState } from "react";
import ProgramForm from "../components/program/ProgramForm";

export default function CreateProgramPage() {
  const [program, setProgram] = useState<any | null>(null);
  const userId = 1; // Remplace par l'user connecté (useAuth().account.id)

  return (
    <div className="p-6">
      {!program ? (
        <ProgramForm userId={userId} onSuccess={setProgram} />
      ) : (
        <div className="max-w-md mx-auto bg-white p-4 rounded shadow">
          <h2 className="text-xl font-bold mb-2">Ton programme personnalisé</h2>
          <p><strong>Objectif :</strong> {program.goal}</p>
          <p><strong>Calories journalières :</strong> {program.daily_calories} kcal</p>
          <p><strong>BMR :</strong> {program.bmr} kcal</p>
          <p><strong>Poids :</strong> {program.weight_kg} kg</p>
          <p><strong>Taille :</strong> {program.height_cm} cm</p>
          <p className="mt-4 text-sm text-gray-500">Tu peux maintenant consulter des recettes adaptées !</p>
        </div>
      )}
    </div>
  );
}
