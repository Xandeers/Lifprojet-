import { BrowserRouter, Route, Routes } from "react-router";
import { AuthStatus, useAuth } from "./hooks/useAuth";
import { useEffect } from "react";
import RegisterPage from "./pages/auth/RegisterPage";
import LoginPage from "./pages/auth/LoginPage.tsx";
import RecipeExplorePage from "./pages/recipe/RecipeExplorePage.tsx";
import MePage from "./pages/auth/MePage.tsx";

export default function App() {
  const { authenticate, status } = useAuth();

  useEffect(() => {
    authenticate();
  }, []);

  if (status == AuthStatus.Unknown) {
    return <p>Chargement...</p>;
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Recipe Routes */}
        <Route path="/" element={<RecipeExplorePage />} />
        {/* Auth Routes */}
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/me" element={<MePage />} />
      </Routes>
    </BrowserRouter>
  );
}
