export type InputProps = {
  name: string;
  id?: string;
  type?: string;
  placeholder?: string;
  required?: boolean;
};

export default function Input({
  name,
  id = name,
  type = "text",
  placeholder = "",
  required = true,
}: InputProps) {
  return <input 
    type={type}
    name={name}
    id={id}
    placeholder={placeholder}
    required={required}
    className="mt-1 w-full border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
  />;
}
