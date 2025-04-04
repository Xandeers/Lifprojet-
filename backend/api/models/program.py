from api.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime
from datetime import datetime, timezone

class FitnessProgram(db.Model):
    __tablename__ = "fitness_programs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    activity_level: Mapped[str] = mapped_column(String(20), nullable=False)
    goal: Mapped[str] = mapped_column(String(20), nullable=False) #le choix prise de masse seche etc ..
    bmr: Mapped[float] = mapped_column(Float, nullable=False) #metabolisme de base base metabolisme rate
    daily_calories: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    #methode serealisation 
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "age": self.age,
            "gender": self.gender,
            "activity_level": self.activity_level,
            "goal": self.goal,
            "bmr": self.bmr,
            "daily_calories": self.daily_calories,
            "created_at": self.created_at.isoformat()
        }
    
    # méthode pour calcule la quantité de prot conseiller par jour 
    def get_protein_requirement(self) -> float:
        coefficients = {
            "cutting": 2.0,
            "bulking": 1.6,
            "maintenance": 1.4
        }
        coefficient = coefficients.get(self.goal, 1.5)
        return round(self.weight_kg * coefficient, 2)

# Fonctions de calcul metabolisme de base ici on a choisi la formule de Mifflin-St Jeor

def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

#recuperation du facteur d'activité 
def get_activity_multiplier(level: str) -> float:
    return {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }.get(level, 1.2)

#permet ajuster en fonction de l'objectif prise de masse suplus calorique ou seche déficite calorique 

def adjust_for_goal(calories: float, goal: str) -> float:
    if goal == "cutting":
        return calories - 500
    elif goal == "bulking":
        return calories + 500
    return calories
