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
import style from "./SignupForm.module.css";

const signupFormSchema = object({
  email: string().email().required(),
  password: string().min(8).required(),
});

type SignupFormSchema = InferType<typeof signupFormSchema>;

type SignupFormProps = {};

export function SignupForm(_: SignupFormProps) {
  const [error, setError] = useState<string>();

  async function handleSubmit(
    values: SignupFormSchema,
    { setSubmitting }: FormikHelpers<SignupFormSchema>,
  ) {
    const { error } = await apiFetch<User, SignupFormSchema>(
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

  const initialValues: SignupFormSchema = {
    email: "",
    password: "",
  };

  return (
    <Formik
      validationSchema={signupFormSchema}
      initialValues={initialValues}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting, submitForm }) => (
        <div className={style.signupForm}>
          <h1>Sign up for an account</h1>
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
            <Button href="/login" variant="secondary">
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
