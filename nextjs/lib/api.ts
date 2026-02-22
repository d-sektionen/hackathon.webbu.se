import qs from "qs";
import { trimEnd, trimStart } from "./util";

export type User = {
  email: string;
  password: string;
};

type Options<K> = Omit<RequestInit, "body"> & { body: K };
type Query = any;

export function apiUrl(path: string, query: Query = {}): string | undefined {
  let base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) return;
  if (!path) return;

  base = trimEnd(base, "/");
  path = trimStart(path, "/");
  console.log({ base, path });

  const url = new URL(`${base}/${path}`);
  url.search = qs.stringify(query);

  return url.href;
}

export async function apiFetch<T = undefined, K = undefined>(
  path: string,
  query?: Query,
  options?: Options<K>,
): Promise<{ data?: T; error?: string }> {
  const url = apiUrl(path, query);
  if (!url) return { error: "Tried to fetch an invalid url" };

  const res = await fetch(url, {
    ...options,
    body: JSON.stringify(options?.body),
  });

  if (!res.ok) {
    return { error: `${res.status} ${res.statusText}` };
  }

  return { data: await res.json() };
}
