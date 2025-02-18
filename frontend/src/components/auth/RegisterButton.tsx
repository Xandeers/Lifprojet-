import { Link } from "react-router";

export default function RegisterButton() {
    return (
        <Link to="/register">
            <button 
                className="hover:cursor-pointer my-3 w-full block outline py-1 outline-gray-300 rounded-md hover:bg-orange-500 bg-orange-400 text-white font-bold">
                S'inscrire
            </button>
        </Link>
    );
}