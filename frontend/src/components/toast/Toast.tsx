type Props = {
    title?: string;
    content: string;
    type?: "success" | "danger" | "default";
};

export default function Toast({title, content, type = "default"} : Props) {
    return (
        <div>
            {title && (
                <p>{title}</p>
            )}
            <p>{content}</p>
        </div>
    );
}