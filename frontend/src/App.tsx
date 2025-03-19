import { BrowserRouter, Route, Routes } from "react-router";
import { AuthStatus, useAuth } from "./hooks/useAuth";
import { useEffect } from "react";
import RegisterPage from "./pages/auth/RegisterPage";
import LoginPage from "./pages/auth/LoginPage.tsx";
import RecipeExplorePage from "./pages/recipe/RecipeExplorePage.tsx";
import MePage from "./pages/auth/MePage.tsx";
import CircleLoader from "./components/layout/CircleLoader.tsx";

export default function App() {
  const { authenticate, status } = useAuth();

  useEffect(() => {
    authenticate();
  }, []);

  if (status == AuthStatus.Unknown) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <CircleLoader />
      </div>
    );
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
