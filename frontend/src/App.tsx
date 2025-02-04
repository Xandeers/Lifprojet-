import { BrowserRouter, Route, Routes } from "react-router";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import { AuthStatus, useAuth } from "./hooks/useAuth";
import { useEffect } from "react";

export default function App() {
    const {authenticate, status} = useAuth();

    useEffect(() => {
        authenticate();
    }, []);

    if (status == AuthStatus.Unknown) {
        return <p>Chargement...</p>
    }
    
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>
        </BrowserRouter>
    );
}