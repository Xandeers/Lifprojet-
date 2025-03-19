import { PropsWithChildren } from "react";
import Header from "./Header.tsx";

export default function Layout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen bg-gray-200 px-4 sm:px-8 md:px-16 lg:px-32 xl:px-64 2xl:px-150">
      <Header />
      <main>{children}</main>
    </div>
  );
}
