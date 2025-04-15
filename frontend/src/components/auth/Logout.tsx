import { Navigate } from "react-router";
import { useToasts } from "../../contexts/ToastContext.tsx";
import { useAuth } from "../../hooks/useAuth.ts";

export default function Logout({ className }: { className: string }) {
  const { logout } = useAuth();
  const { pushToast } = useToasts();
  const handleClick = () => {
    logout();
    pushToast({
      type: "success",
      content: "Vous avez été deconnecté",
    });
    return <Navigate to="/" replace />;
  };
  return (
    <p onClick={handleClick} className={className}>
      Se deconnecter
    </p>
  );
}
