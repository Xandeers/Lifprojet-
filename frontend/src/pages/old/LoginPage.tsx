import { Navigate } from "react-router";
import LoginForm from "../../components/auth/LoginForm";
import { AuthStatus, useAuth } from "../../hooks/useAuth";
import LayoutPage from "./LayoutPage";

export default function LoginPage() {
    const {status} = useAuth();

    if(status === AuthStatus.Authenticated) {
        return <Navigate to="/" replace />;
    }

    return (
        <LayoutPage title="Se connecter">
            <div className="p-5">
                <LoginForm />
            </div>
        </LayoutPage>
    );
}