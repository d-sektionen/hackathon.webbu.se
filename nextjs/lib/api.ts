import qs from "qs";
import { trimEnd, trimStart } from "./util";

export type User = {
  email: string;
  password: string;
};

export type Session = {
  user: User;
};

type Options<K> = Omit<RequestInit, "body"> & {
  method: RequestInit["method"];
  body?: K;
};
type Query = any;

export function apiUrl(path: string, query: Query = {}): string | undefined {
  let base =
    process.env.INTERNAL_API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) return;
  if (!path) return;

  base = trimEnd(base, "/");
  path = trimStart(path, "/");

  const url = new URL(`${base}/${path}`);
  url.search = qs.stringify(query);

  return url.href;
}

export async function apiFetch<T = undefined, K = unknown>(
  path: string,
  query?: Query,
  options: Options<K> = { method: "GET", headers: {} },
): Promise<{ data?: T; error?: string }> {
  const url = apiUrl(path, query);
  if (!url) return { error: "Tried to fetch an invalid url" };

  // Janky workaround to make cookies work in server components
  if (typeof window === "undefined") {
    const { cookies } = await import("next/headers");
    const store = await cookies();
    const cks = store.getAll();
    options.headers = {
      ...options.headers,
      Cookie: cks.map((c) => `${c.name}=${c.value}`).join("; "),
    };
  }

  console.log(options.method, url, options.headers);

  const res = await fetch(url, {
    ...options,
    credentials: "include",
    body: JSON.stringify(options?.body),
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    return { error: `${res.status} ${res.statusText}` };
  }

  return { data: await res.json() };
}

export async function getSession(): Promise<Session | undefined> {
  const { data } = await apiFetch<Session>("/me", {});
  return data;
}
