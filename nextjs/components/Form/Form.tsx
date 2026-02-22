import clsx from "clsx";
import { Form as FormikForm, type FormikFormProps } from "formik";
import style from "./Form.module.css";
import { HiMiniExclamationTriangle, HiMiniXMark } from "react-icons/hi2";

type FormProps = { error?: string; submitting?: boolean } & FormikFormProps;

export function Form({
  className,
  submitting,
  error,
  children,
  ...rest
}: FormProps) {
  return (
    <FormikForm
      {...rest}
      className={clsx(style.form, submitting && style.submitting, className)}
    >
      {error ? (
        <div className={style.error}>
          <HiMiniExclamationTriangle className={style.icon} />
          <p>{error}</p>
        </div>
      ) : null}
      {children}
    </FormikForm>
  );
}
