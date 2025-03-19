import { useToasts } from "../../contexts/ToastContext.tsx";
import Form from "../../components/layout/Form.tsx";
import Layout from "../../components/layout/Layout.tsx";
import { useAuth } from "../../hooks/useAuth.ts";

export default function LoginPage() {
  const { login } = useAuth();

  const handleLogin = async (formData: Record<string, FormDataEntryValue>) => {
    login(formData.email as string, formData.password as string);
  };

  return (
    <Layout guestRequired>
      <h1 className="text-3xl font-semibold pb-3">Connexion</h1>
      <Form
        fields={[
          {
            name: "email",
            label: "Adresse E-mail",
            type: "email",
            placeholder: "exemple@mail.com",
          },
          {
            name: "password",
            label: "Mot de passe",
            type: "password",
            placeholder: "••••••••",
          },
        ]}
        onSubmit={handleLogin}
        submitText="Se connecter"
      />
    </Layout>
  );
}
