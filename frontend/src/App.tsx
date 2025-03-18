import { BrowserRouter, Route, Routes } from "react-router";
import { AuthStatus, useAuth } from "./hooks/useAuth";
import { useEffect } from "react";
import RegisterPage from "./pages/auth/RegisterPage";

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
                <Route path="/register" element={<RegisterPage />} />
            </Routes>
        </BrowserRouter>
    );
}