const baseURL = "http://127.0.0.1:5000";

export async function fetchAPI<T>(
  method: "GET" | "POST" | "PUT" | "DELETE",
  endpoint: string,
  data?: Record<string, unknown>
): Promise<T> {
  const body = data ? JSON.stringify(data) : undefined;
  const r = await fetch(baseURL + endpoint, {
    method,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "include",
    body,
  });
  if (r.ok) return r.json() as Promise<T>;
  throw new ApiError(r.status, await r.json());
}

class ApiError extends Error {
  constructor(public status: number, public data: Record<string, unknown>) {
    super();
  }
}
