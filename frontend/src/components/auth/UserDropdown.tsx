import { useState } from "react";
import { AuthStatus, useAuth } from "../../hooks/useAuth.ts";
import { Link } from "react-router";
import Logout from "./Logout.tsx";
export default function UserDropdown() {
  const { status } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  const handleClick = () => {
    setShowMenu(!showMenu);
  };
  const menuItemClasses =
    "w-full p-3 text-center border border-gray-200 hover:bg-gray-100 cursor-pointer";
  return (
    <div className="flex flex-col relative">
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"
        alt="profile image"
        className="w-9 rounded-3xl cursor-pointer shadow-xs"
        onClick={handleClick}
      />
      {showMenu && (
        <div
          className="absolute top-full right-0 mt-2 bg-white shadow-lg border border-gray-300 
                    rounded-lg z-50 w-48 md:w-72
                    max-sm:min-w-screen"
        >
          {status === AuthStatus.Guest && (
            <div onClick={handleClick} className="text-sm flex flex-col">
              <Link className={menuItemClasses} to="/me">
                Se connecter
              </Link>
              <Link className={menuItemClasses} to="/register">
                S'inscrire
              </Link>
            </div>
          )}
          {status === AuthStatus.Authenticated && (
            <div onClick={handleClick} className="text-sm flex flex-col">
              <Link className={menuItemClasses} to="/me">
                Mon profile
              </Link>
              <Logout className={menuItemClasses} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
