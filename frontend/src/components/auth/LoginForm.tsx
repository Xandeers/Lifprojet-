import { FormEventHandler } from "react";
import { useAuth } from "../../hooks/useAuth";

export default function LoginForm() {
    const {login} = useAuth();
    const handleSubmit: FormEventHandler<HTMLFormElement> = (e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        login(data.get("email")!.toString(), data.get("password")!.toString());
    };

    return (
        <>
            <div style={{ color: 'red' }} id="error-message"></div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="email">Adresse Email:</label>
                <input type="email"
                name="email"
                placeholder="Email" 
                /> <br />
                <label htmlFor="password">Mot de passe:</label>
                <input type="password"
                name="password"
                placeholder="Mot de passe"
                /> <br />
            <button type="submit">Se connecter</button>
        </form>
        </>
    );
}
