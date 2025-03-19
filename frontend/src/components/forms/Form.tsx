import { FormEvent } from "react";
import Input, { InputProps } from "./Input.tsx";

type Field = InputProps & {
  label: string;
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
      className="rounded-lg space-y-4"
    >
      {fields.map(({ name, label, type = "text", placeholder, required = true }: Field) => (
        <div key={name}>
          <label htmlFor={name} className="block font-medium text-gray-700">
            {label}
          </label>
          <Input
            type={type}
            name={name}
            placeholder={placeholder}
            required={required}
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
