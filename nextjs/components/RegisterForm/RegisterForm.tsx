/** biome-ignore-all lint/suspicious/noThenProperty: yup uses "then" for conditional schemas */
"use client";

import { Formik, type FormikHelpers } from "formik";
import { boolean, type InferType, object, string } from "yup";
import type { User } from "@/lib/api";
import { TextField } from "../TextField/TextField";
import style from "./RegisterForm.module.css";
import { Button } from "../Button/Button";
import { Form } from "../Form/Form";

const registerFormSchema = object({
  firstName: string().required(),
  lastNames: string().required(),
  email: string().email().required(),
  hasLiuId: boolean(),
  liuId: string()
    .matches(/[a-z]{5}[0-9]{3}/)
    .when("hasLiuId", { is: true, then: (s) => s.required() }),
});

type RegisterFormSchema = InferType<typeof registerFormSchema>;

type RegisterFormProps = {
  onRegister?: (user: User) => void;
};

export function RegisterForm({ onRegister }: RegisterFormProps) {
  function handleSubmit(
    _values: RegisterFormSchema,
    { setSubmitting }: FormikHelpers<RegisterFormSchema>,
  ) {
    setSubmitting(true);
    // do something with values
    setSubmitting(false);
    onRegister?.({});
  }

  const initialValues: RegisterFormSchema = {
    firstName: "",
    lastNames: "",
    email: "",
    hasLiuId: false,
    liuId: undefined,
  };

  return (
    <Formik
      validationSchema={registerFormSchema}
      initialValues={initialValues}
      onSubmit={handleSubmit}
    >
      <Form className={style.registerForm}>
        <TextField cols={3} label="First Name" name="firstName" />
        <TextField cols={3} label="Last Name(s)" name="lastNames" />
        <TextField cols={6} label="E-mail" name="email" />

        <div className={style.buttons}>
          <Button type="submit" key={0} variant="primary">
            Submit
          </Button>
        </div>
      </Form>
    </Formik>
  );
}
