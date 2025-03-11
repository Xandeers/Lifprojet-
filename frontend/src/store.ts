import { create } from "zustand";
import { combine } from "zustand/middleware";
import { Account } from "./hooks/useAuth";

export const useAccountStore = create(
    combine(
        {
                account: undefined as undefined | null | Account,
            },
            (set) => ({
                setAccount: (account: Account | null) => set({ account 
                })
            })
        ),

);