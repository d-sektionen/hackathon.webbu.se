"use client";

import { apiFetch } from "@/lib/api";
import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import style from "./ProjectPage.module.css";
import DOMPurify from "dompurify";
import { marked } from "marked";

// TODO: this is duplicated from components/ProjectList/ProjectList.tsx
interface Project {
  id: string;
  name: string;
  description: string;
  github_url: string;
  owner_user_id: string;
  created_at: string;
}

export default function ProjectList({ id }: { id: string }) {
  let [project, setProject] = useState<Project>();
  let [readme, setReadme] = useState<string>();
  let readmeHTML = useMemo<string>(
    () => DOMPurify.sanitize(marked.parse(readme ?? "") as string),
    [readme],
  );
  let [error, setError] = useState<string>();

  useEffect(() => {
    apiFetch<{ project: Project }>(`/projects/${encodeURIComponent(id)}`).then(
      ({ data, error }) => {
        setProject(data?.project);
        if (error === undefined) {
          setError(error);
        }
      },
    );

    apiFetch<{ content: string }>(
      `/projects/${encodeURIComponent(id)}/readme`,
    ).then(({ data, error }) => {
      setReadme(data?.content);
      if (error === undefined) {
        setError(error);
      }
    });
  }, []);

  if (error !== undefined) {
    return <strong>Error {error}</strong>;
  }
  if (project === undefined) {
    return <strong>Loading projects...</strong>;
  }

  return (
    <>
      <h1 className={style.title}>{project.name}</h1>
      <article className={style.project}>
        <p>{project.description}</p>

        <div
          className={style.readme}
          dangerouslySetInnerHTML={{ __html: readmeHTML }}
        ></div>
      </article>
    </>
  );
}
