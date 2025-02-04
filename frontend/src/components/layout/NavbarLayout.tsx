import { Link } from "react-router";
import { AuthStatus, useAuth } from "../../hooks/useAuth";
import LogoutButton from "../auth/LogoutButton";

export default function NavbarLayout() {
    const { status } = useAuth();
    let button;
    if(status === AuthStatus.Authenticated) {
        button = <LogoutButton />
    }
    return (
        <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/login">Login</Link></li>
            {button}
        </ul>
    );
}