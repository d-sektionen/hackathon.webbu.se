"use client";

import { apiFetch } from "@/lib/api";
import { useEffect, useState } from "react";
import Link from "next/link";
import style from "./ProjectList.module.css";

interface Project {
  id: string;
  name: string;
  description: string;
  github_url: string;
  owner_user_id: string;
  created_at: string;
}

export default function ProjectList() {
  let [projects, setProjects] = useState<Project[]>();
  let [error, setError] = useState<string>();

  useEffect(() => {
    apiFetch<{ projects: Project[] }>("/projects").then(({ data, error }) => {
      setProjects(data?.projects);
      setError(error);
    });
  }, []);

  if (error !== undefined) {
    return <strong>Error {error}</strong>;
  }
  if (projects === undefined) {
    return <strong>Loading projects...</strong>;
  }
  return (
    <>
      <h1 className={style.pageTitle}>Projects</h1>
      <div className={style.projectList}>
        {projects.map((project) => (
          <Link
            key={project.id}
            className={style.project}
            href={`/projects/${project.id}`}
          >
            <h1>{project.name}</h1>
            <p>{project.description}</p>
          </Link>
        ))}
      </div>
    </>
  );
}
