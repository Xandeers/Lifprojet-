import { PropsWithChildren } from "react";
import Header from "./Header.tsx";
import { AuthStatus, useAuth } from "../../hooks/useAuth.ts";
import { Navigate } from "react-router";

export default function Layout({
  children,
  guestRequired = false,
}: PropsWithChildren & { guestRequired?: boolean }) {
  const { status } = useAuth();

  if ((guestRequired && status != AuthStatus.Guest) || AuthStatus.Unknown)
    return <Navigate to="/" replace />;

  return (
    <>
      <Header />
      <div className="pt-8 min-h-screen bg-blue-50 px-4 sm:px-8 md:px-16 lg:px-32 xl:px-64 2xl:px-150">
        <main className="border border-gray-200 rounded-lg shadow-xs p-10 bg-white">
          {children}
        </main>
      </div>
    </>
  );
}
