import { BrowserRouter, Route, Routes } from "react-router";
import { AuthStatus, useAuth } from "./hooks/useAuth";
import { useEffect } from "react";
import RegisterPage from "./pages/auth/RegisterPage";
import LoginPage from "./pages/auth/LoginPage.tsx";
import MePage from "./pages/auth/MePage.tsx";
import CircleLoader from "./components/layout/CircleLoader.tsx";
import NotFoundPage from "./pages/error/NotFoundPage.tsx";
import RecipePage from "./pages/recipe/RecipePage.tsx";
import RecipeFeedPage from "./pages/recipe/RecipeFeedPage.tsx";
import RecipeCreatePage from "./pages/recipe/RecipeCreatePage";

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
        <Route path="/" element={<RecipeFeedPage />} />
        <Route path="/recipe/:slug" element={<RecipePage />} />
        <Route path="/recipe/create" element={<RecipeCreatePage />} />
        {/* Auth Routes */}
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/me" element={<MePage />} />
        {/* 404 Not Found */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
