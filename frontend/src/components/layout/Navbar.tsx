import { Link, Links } from "react-router";

export default function Navbar() {
    return (
        <nav>
            <h1>Lifprojet</h1>
            <ul>
                <li><Link to="/register">Register</Link></li>
            </ul>
        </nav>
    );
}