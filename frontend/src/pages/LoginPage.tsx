import { Navigate } from "react-router";
import LoginForm from "../components/auth/LoginForm";
import { AuthStatus, useAuth } from "../hooks/useAuth";
import LayoutPage from "./LayoutPage";

export default function LoginPage() {
    const {status} = useAuth();

    if(status === AuthStatus.Authenticated) {
        return <Navigate to="/" replace />;
    }

    return (
        <LayoutPage>
            <h1 className="font-bold text-3xl">Login Page</h1>
            <LoginForm />
        </LayoutPage>
    );
}