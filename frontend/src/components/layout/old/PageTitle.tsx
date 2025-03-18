type Props = {
    title: string;
};

export function PageTitle({title}: Props) {
    return (
        <h1 className="text-xl font-bold block border-b border-gray-200 p-5">
            {title}
        </h1>
    );
}