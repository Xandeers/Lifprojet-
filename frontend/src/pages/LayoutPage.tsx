import { ReactNode } from "react";
import HeaderComponent from "../components/layout/HeaderLayout";

function LayoutPage( {children }: {children: ReactNode}) {
    return (
        <>
            <HeaderComponent />
            <main>
                {children}
            </main>
        </>
    );
}

export default LayoutPage;