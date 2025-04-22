import { Link } from "react-router";
import UserDropdown from "../auth/UserDropdown.tsx";

export default function Navbar() {
  return (
    <nav className="flex justify-between p-5 items-center">
      <h1 className="text-xl font-bold">Scoreat</h1>
      <ul className="flex space-x-4 text-lg text-gray-600 gap-5 items-center">
        <li className="hover:text-gray-800">
          <Link to="/">Explorer</Link>
        </li>
        <UserDropdown />
      </ul>
    </nav>
  );
}
