import { Link } from "react-router";

export default function LoginButton() {
    return (
        <Link to="/login">
            <button 
                className="hover:cursor-pointer w-full block outline py-1 outline-gray-300 rounded-md hover:bg-gray-100">
                Se connecter
            </button>
        </Link>
    );
}