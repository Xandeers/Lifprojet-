import { PropsWithChildren } from "react";
import Header from "../components/layout/Header";

export default function Layout({ children } : PropsWithChildren) {
  return (
    <>
    <div>
      <Header />
      <main>
        {children}
      </main>
    </div>
    </>
  );
}