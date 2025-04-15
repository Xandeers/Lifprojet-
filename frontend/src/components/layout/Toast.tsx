import clsx from "clsx";

type Props = {
  title?: string;
  content: string;
  type?: "success" | "danger" | "default";
};

export default function Toast({ title, content, type = "default" }: Props) {
  return (
    <div
      className={clsx(
        "p-4 rounded-md w-sm shadow-sm",
        type === "default" && "bg-gray-100",
        type === "success" && "bg-green-600 text-white",
        type === "danger" && "bg-red-500 text-white"
      )}
    >
      {title && <p className="font-bold text-xl py-1">{title}</p>}
      <p>{content}</p>
    </div>
  );
}
