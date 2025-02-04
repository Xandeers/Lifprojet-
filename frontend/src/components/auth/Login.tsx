import React, { useState } from "react";
import API from "../../utils/api";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await API.post("/login", {email, password});
            alert("Connexion réussie !");
        } catch (err) {
            setErrorMessage((err as any).response?.data?.message || "Erreur de connexion");
        }
    };

    return (
        <>
            <div style={{ color: 'red' }} id="error-message">{errorMessage}</div>
            <form onSubmit={handleLogin}>
                <label htmlFor="email">Adresse Email:</label>
                <input type="email"
                name="email"
                placeholder="Email" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
                /> <br />
                <label htmlFor="password">Mot de passe:</label>
                <input type="password"
                name="password"
                placeholder="Mot de passe"
                value={password}
                onChange={e => setPassword(e.target.value)}
                /> <br />
            <button type="submit">Se connecter</button>
        </form>
        </>
    );
}