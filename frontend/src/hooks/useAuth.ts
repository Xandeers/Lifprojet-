import { useCallback } from "react";
import { useAccountStore } from "../store";
import { fetchAPI } from "../utils/api.ts";
import { useToasts } from "../contexts/ToastContext.tsx";

export type Account = {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
};

export enum AuthStatus {
  Unknown = 0,
  Authenticated = 1,
  Guest = 2,
}

export function useAuth() {
  const { account, setAccount } = useAccountStore();
  const { pushToast } = useToasts();
  let status;
  switch (account) {
    case null:
      status = AuthStatus.Guest;
      break;
    case undefined:
      status = AuthStatus.Unknown;
      break;
    default:
      status = AuthStatus.Authenticated;
      break;
  }

  const authenticate = useCallback(() => {
    fetchAPI<Account>("GET", "/auth/me")
      .then(setAccount)
      .catch(() => setAccount(null));
  }, []);

  const login = useCallback((email: string, password: string) => {
    fetchAPI<Account>("POST", "/auth/login", { email, password })
      .then((data) => {
        setAccount(data);
        pushToast({
          content: `Salut ${data.username} !`,
          type: "success",
        });
      })
      .catch((err) => {
        setAccount(null);
        pushToast({
          title: "Erreur de connexion",
          content: JSON.stringify(err),
          type: "danger",
        });
      });
  }, []);

  const logout = useCallback(() => {
    fetchAPI("DELETE", "/auth/logout").then(() => setAccount(null));
  }, []);

  return {
    account,
    status,
    authenticate,
    login,
    logout,
  };
}
