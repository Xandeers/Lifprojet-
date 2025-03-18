import { FormEvent } from "react";
import Layout from "../Layout";
import { useToasts } from "../../contexts/ToastContext";

export default function RegisterPage() {

  const { pushToast } = useToasts();

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const username = formData.get('username');
    const email = formData.get('email');
    const password = formData.get('password');
    
    pushToast({
      title: 'Nice',
      content: "good",
      duration: 1
    });
  };
  
  return (
    <Layout>
    <h1>Inscription</h1>
    <form onSubmit={onSubmit}>
      <div>
        <label htmlFor="username">Nom d'utilisateur</label>
        <input type="text" name="username" />
      </div> <br />
      <div>
        <label htmlFor="email">Adresse E-mail</label>
        <input type="email" name="email" />
      </div> <br />
      <div>
        <label htmlFor="password">Mot de passe</label>
        <input type="password" name="email" />
      </div> <br />
      <button type="submit">S'inscrire</button>
    </form>
    </Layout>
  );
}