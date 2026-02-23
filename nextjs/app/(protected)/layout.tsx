import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getSession } from "@/lib/api";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getSession();
  if (!session) {
    redirect("/login");
  }

  return <>{children}</>;
}
