import { useToasts } from "../../contexts/ToastContext.tsx";
import Form from "../../components/layout/Form.tsx";
import Layout from "../../components/layout/Layout.tsx";
import { fetchAPI } from "../../utils/api.ts";
import { Account } from "../../hooks/useAuth.ts";
import { Navigate } from "react-router";

export default function RegisterPage() {
  const { pushToast } = useToasts();

  const handleRegister = (formData: Record<string, FormDataEntryValue>) => {
    fetchAPI<Account>("POST", "/auth/register", formData)
      .then(() => {
        pushToast({
          content: "Inscription réalisée avec succès",
          type: "success",
        });
        return <Navigate to="/" replace />;
      })
      .catch((err) =>
        pushToast({
          title: "Erreur lors de l'inscription",
          content: JSON.stringify(err),
          type: "danger",
        })
      );
  };

  return (
    <Layout guestRequired>
      <h1 className="text-3xl font-semibold pb-3">Inscription</h1>
      <Form
        fields={[
          {
            name: "username",
            label: "Nom d'utilisateur",
            placeholder: "Entrez votre nom",
          },
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
        onSubmit={handleRegister}
        submitText="S'inscrire"
      />
    </Layout>
  );
}
