import { FormEventHandler } from "react";
import { useAuth } from "../../hooks/useAuth";

export default function LoginForm() {
    const {login} = useAuth();
    const handleSubmit: FormEventHandler<HTMLFormElement> = (e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        login(data.get("email")!.toString(), data.get("password")!.toString());
    };

    const inputClassName = "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus-:-outline-offset-2 focus:outline-indigo-400 sm:text-sm/6";
    const labelClassName = "block text-sm/6 font-medium text-gray-900";
    const submitClassName = "block hover:cursor-pointer bg-orange-400 hover:bg-orange-300 w-full rounded-md py-2 text-white font-bold";
    return (
        <>
            <div style={{ color: 'red' }} id="error-message"></div>
            <form onSubmit={handleSubmit}>
                <label htmlFor="email" className="">Adresse e-mail:</label>
                <div className="mt-2">
                    <input type="email"
                        name="email"
                        placeholder="toto@toto.com"
                        className={inputClassName}
                    />
                </div>
                <br />
                <div className="mt-2">
                <label htmlFor="password" className={labelClassName}>Mot de passe:</label>
                <input type="password"
                    name="password"
                    placeholder="Mot de passe"
                    className={inputClassName}
                />
                </div>
                <br />
            <button type="submit" className={submitClassName}>Se connecter</button>
        </form>
        </>
    );
}
