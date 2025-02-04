import { useCallback } from "react";
import { useAccountStore } from "../store";
import API from "../utils/api";

export type Account = {
    id: number,
    username: string,
    email: string,
    is_admin: boolean
};

export enum AuthStatus {
    Unknown = 0,
    Authenticated = 1,
    Guest = 2
};

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
        API.get<Account>('/auth/profile')
            .then(res => setAccount(res.data))
            .catch(() => setAccount(null));
    }, []);

    const login = useCallback((email: string, password: string) => {
        API.post<Account>('/auth/login', {email, password})
            .then(res => setAccount(res.data))
            .catch(() => setAccount(null));
    }, []);

    const logout = useCallback(() => {
        API.delete('/auth/logout')
            .then(() => setAccount(null));
    }, []);

    return {
        account,
        status,
        authenticate,
        login,
        logout,
    }
}