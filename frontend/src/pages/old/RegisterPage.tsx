import RegisterForm from "../../components/auth/RegisterForm";
import LayoutPage from "./LayoutPage";

export default function RegisterPage() {
    return (
        <LayoutPage title="S'inscrire">
            <RegisterForm />
        </LayoutPage>
    );
}