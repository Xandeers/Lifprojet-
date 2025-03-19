import { FormEvent } from "react";

type Field = {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
};

type Props = {
  fields: Field[];
  onSubmit: (data: Record<string, FormDataEntryValue>) => void;
  submitText?: string;
};

export default function Form({
  fields,
  onSubmit,
  submitText = "Soumettre",
}: Props) {
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());
    onSubmit(data);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-6 rounded-lg shadow-md space-y-4"
    >
      {fields.map(({ name, label, type = "text", placeholder }: Field) => (
        <div key={name}>
          <label htmlFor={name} className="block font-medium text-gray-700">
            {label}
          </label>
          <input
            type={type}
            name={name}
            id={name}
            placeholder={placeholder}
            className="mt-1 w-full border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      ))}
      <button
        type="submit"
        className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 cursor-pointer"
      >
        {submitText}
      </button>
    </form>
  );
}
