import clsx from "clsx";
import { Form as FormikForm, type FormikFormProps } from "formik";
import style from "./Form.module.css";
import { ReactElement } from "react";

type FormProps = {} & FormikFormProps;

export function Form({ className, buttons, children, ...rest }: FormProps) {
  return (
    <FormikForm {...rest} className={clsx(style.form, className)}>
      {children}
    </FormikForm>
  );
}
