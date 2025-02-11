import { Link } from "react-router";

type Props = {
    title: string;
    logo: string;
    dest: string;
};

export default function NavbarItem({title, logo, dest}: Props) {
    return (
        <Link to={dest} className="flex space-x-3 text-lg font-semibold p-2 rounded-xl hover:bg-gray-100">
            <span>{logo}</span>
            <span>{title}</span>
        </Link>
    );
}