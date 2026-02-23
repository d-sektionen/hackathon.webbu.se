/** biome-ignore-all lint/suspicious/noThenProperty: yup uses "then" for conditional schemas */
"use client";

import { Formik, type FormikHelpers } from "formik";
import { redirect } from "next/navigation";
import { useState } from "react";
import { type InferType, object, string } from "yup";
import { apiFetch, type User } from "@/lib/api";
import { Button } from "../Button/Button";
import { Form } from "../Form/Form";
import { TextField } from "../TextField/TextField";
import style from "./LoginForm.module.css";

const loginFormSchema = object({
  email: string().email().required(),
  password: string().min(8).required(),
});

type LoginFormSchema = InferType<typeof loginFormSchema>;

type LoginFormProps = {};

export function LoginForm(_: LoginFormProps) {
  const [error, setError] = useState<string>();

  async function handleSubmit(
    values: LoginFormSchema,
    { setSubmitting }: FormikHelpers<LoginFormSchema>,
  ) {
    const { error } = await apiFetch<User, LoginFormSchema>(
      "/login",
      undefined,
      { method: "POST", body: values },
    );
    setSubmitting(false);

    if (error) {
      setError(error);
    } else {
      redirect("/dashboard");
    }
  }

  const initialValues: LoginFormSchema = {
    email: "",
    password: "",
  };

  return (
    <Formik
      validationSchema={loginFormSchema}
      initialValues={initialValues}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting, submitForm }) => (
        <div className={style.loginForm}>
          <h1>Log in to your account</h1>
          <Form submitting={isSubmitting} error={error}>
            <TextField cols={6} label="E-mail" type="email" name="email" />
            <TextField
              cols={6}
              label="Password"
              type="password"
              name="password"
            />
          </Form>
          <div className={style.buttons}>
            <Button href="/signup" variant="secondary">
              Don't have an account?
            </Button>
            <Button onClick={submitForm} type="submit" variant="primary">
              Login
            </Button>
          </div>
        </div>
      )}
    </Formik>
  );
}
