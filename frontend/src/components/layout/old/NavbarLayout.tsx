import { AuthStatus, useAuth } from "../../../hooks/useAuth";
import LoginButton from "../../auth/LoginButton";
import LogoutButton from "../../auth/LogoutButton";
import RegisterButton from "../../auth/RegisterButton";
import NavbarItem from "./NavbarItem";

export default function NavbarLayout() {
    const { status, account } = useAuth();
    let button;
    if(status === AuthStatus.Authenticated) {
        button = <LogoutButton />
    }
    return (
        <nav className="w-64 h-full p-4 bg-white border-r border-gray-200 flex flex-col fixed">
            <div className="mb-6">
                <img src="logo.png" alt="RecipeLogo" />
            </div>
            <ul className="space-y-4">
                <li><NavbarItem title="Accueil" logo="🏠" dest="/" /></li>
                <li><NavbarItem title="Explorer" logo="🍽️" dest="/" /></li>
                <li>
                    {
                        account != undefined 
                            ? <NavbarItem title={account.username} logo="👤"dest= "/" /> 
                            : <>
                                <RegisterButton />
                                <LoginButton />                                  
                              </>
                    }
                </li>
            </ul>
        </nav>
    );
}