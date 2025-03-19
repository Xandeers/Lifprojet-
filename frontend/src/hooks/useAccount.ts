import { useNavigate } from "react-router";
import { useAuth } from "./useAuth";

export function useAccount() {
  const { account } = useAuth();
  const navigate = useNavigate();
  if (!account) {
    navigate("/");
  }

  const isAdmin = (): boolean | undefined => {
    return account?.is_admin;
  };

  return {
    account,
    isAdmin,
  };
}
