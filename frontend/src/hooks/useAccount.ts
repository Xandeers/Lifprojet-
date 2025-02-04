import { useAuth } from "./useAuth";

export function useAccount() {
    const {account} = useAuth();

    if(!account) {
        throw new Error("User not authenticated");
    }

    const isAdmin = (): boolean => {
        return account?.is_admin;
    };

    return {
        account,
        isAdmin
    }
}