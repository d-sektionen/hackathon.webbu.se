import ProjectPage from "@/components/ProjectPage/ProjectPage";

export default async function projectsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <main className="container">
      <ProjectPage id={id} />
    </main>
  );
}
