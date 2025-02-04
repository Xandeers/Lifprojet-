import { Link } from "react-router";

export default function NavbarLayout() {
    return (
        <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/login">Login</Link></li>
        </ul>
    );
}