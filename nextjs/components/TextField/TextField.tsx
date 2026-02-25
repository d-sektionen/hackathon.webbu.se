import clsx from "clsx";
import { Field, type FieldProps } from "formik";
import type { CSSProperties, InputHTMLAttributes } from "react";
import style from "./TextField.module.css";

type TextFieldProps = {
  label: string;
  className?: string;
  cols?: number;
} & InputHTMLAttributes<never>;

export function TextField({
  cols = 6,
  label,
  className,
  ...rest
}: TextFieldProps) {
  return (
    <Field {...rest}>
      {({ field, form: { touched, errors } }: FieldProps<string>) => {
        const wasTouched = Object.hasOwn(touched, field.name);
        const hasErrors = Object.hasOwn(errors, field.name);

        return (
          <div
            style={{ "--cols": cols } as CSSProperties}
            className={clsx(
              style.textField,
              wasTouched && style.touched,
              wasTouched && hasErrors && style.invalid,
              className,
            )}
          >
            {label ? <p className={style.label}>{label}</p> : null}
            <input {...field} {...rest} />
            {wasTouched && hasErrors ? (
              <p className={style.error}>{String(errors[field.name])}</p>
            ) : null}
          </div>
        );
      }}
    </Field>
  );
}
