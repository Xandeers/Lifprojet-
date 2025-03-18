import { type ReactNode } from "react";
import HeaderComponent from "../../components/layout/old/HeaderLayout";
import { PageTitle } from "../../components/layout/old/PageTitle";

type Props = {
    title: string;
    children: ReactNode;
};

function LayoutPage( { title, children }: Props) {
    return (
        <div className="container mx-auto max-w-6xl flex flex-row">
            <HeaderComponent />
            <main className="flex-1 ml-64 border-r min-h-screen flex-column border-gray-200 max-w-2xl">
                <PageTitle title={title} />
                {children}
            </main>
        </div>
    );
}

export default LayoutPage;