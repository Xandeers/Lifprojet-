import { useCallback } from "react";
import { useAccountStore } from "../store";
import fetchAPI from "../utils/api.ts";

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
    fetchAPI("GET", "/auth/me")
      .then(async (res) => setAccount(await res.json()))
      .catch(() => setAccount(null));
  }, []);

  const login = useCallback((email: string, password: string) => {
    fetchAPI("POST", "/auth/login", { email, password })
      .then(async (res) => setAccount(await res.json()))
      .catch(() => setAccount(null));
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
