/** biome-ignore-all lint/suspicious/noThenProperty: yup uses "then" for conditional schemas */
"use client";

import { Formik, type FormikHelpers } from "formik";
import { useState } from "react";
import { boolean, type InferType, object, string } from "yup";
import { apiFetch, type User } from "@/lib/api";
import { Button } from "../Button/Button";
import { Form } from "../Form/Form";
import { TextField } from "../TextField/TextField";
import style from "./RegisterForm.module.css";
import { redirect } from "next/navigation";

const registerFormSchema = object({
  email: string().email().required(),
  password: string().min(8).required(),
});

type RegisterFormSchema = InferType<typeof registerFormSchema>;

type RegisterFormProps = {};

export function RegisterForm(_: RegisterFormProps) {
  const [error, setError] = useState<string>();

  async function handleSubmit(
    values: RegisterFormSchema,
    { setSubmitting }: FormikHelpers<RegisterFormSchema>,
  ) {
    const { error } = await apiFetch<User, RegisterFormSchema>(
      "/signup",
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

  const initialValues: RegisterFormSchema = {
    email: "",
    password: "",
  };

  return (
    <Formik
      validationSchema={registerFormSchema}
      initialValues={initialValues}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting, submitForm }) => (
        <div className={style.registerForm}>
          <h1>Register for an account</h1>
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
            <Button href="/signin" variant="secondary">
              Already have an account?
            </Button>
            <Button onClick={submitForm} type="submit" variant="primary">
              Sign up
            </Button>
          </div>
        </div>
      )}
    </Formik>
  );
}
