import { useToasts } from "../../contexts/ToastContext";
import fetchAPI from "../../utils/api.ts";
import Form from "../../components/layout/Form.tsx";
import Layout from "../../components/layout/Layout.tsx";

export default function RegisterPage() {
  const { pushToast } = useToasts();

  const handleRegister = async (
    formData: Record<string, FormDataEntryValue>
  ) => {
    const res = await fetchAPI("POST", "/auth/register", formData);
    const data = await res.json();
    if (!res.ok) {
      pushToast({
        title: "Erreur",
        content: JSON.stringify(data),
        duration: 2,
        type: "danger",
      });
    } else {
      pushToast({
        title: "Succès",
        content: "vous avez correctemennt été inscris",
        duration: 2,
        type: "success",
      });
    }
  };

  return (
    <Layout>
      <h1>Inscription</h1>
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
