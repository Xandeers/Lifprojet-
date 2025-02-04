import Login from "../components/auth/Login";
import LayoutPage from "./LayoutPage";

export default function LoginPage() {
    return (
        <LayoutPage>
            <h1 className="font-bold text-3xl">Login Page</h1>
            <Login />
        </LayoutPage>
    );
}