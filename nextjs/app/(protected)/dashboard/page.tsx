import { getSession } from "@/lib/api";

export default async function DashboardPage() {
	const session = await getSession();
	if (session == null) {
		return;
	}

	return <main className="container"></main>;
}
