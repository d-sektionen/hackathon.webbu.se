import clsx from "clsx";
import type { ButtonHTMLAttributes } from "react";
import type { IconType } from "react-icons";
import style from "./Button.module.css";

type ButtonProps = {
  icon?: IconType;
  href?: string;
  variant?: "primary" | "secondary" | "link";
} & ButtonHTMLAttributes<never>;

export function Button({
  children,
  variant = "secondary",
  icon: Icon,
  href,
  type = "button",
  className,
  ...rest
}: ButtonProps) {
  const Component = href ? "a" : "button";

  return (
    <Component
      {...rest}
      href={href}
      type={type}
      className={clsx(
        className,
        style.button,
        Icon && style.hasIcon,
        children && style.hasText,
        `variant-${variant}`,
      )}
    >
      {Icon && <Icon size={20} />}
      {children}
    </Component>
  );
}
