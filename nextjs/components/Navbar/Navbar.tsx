import clsx from "clsx";
import Image from "next/image";
import Link from "next/link";
import { HiMiniBars3 } from "react-icons/hi2";
import { Button } from "../Button/Button";
import style from "./Navbar.module.css";

type NavbarProps = {
  links?: { label: string; href: string }[];
};

export function Navbar({ links = [] }: NavbarProps) {
  return (
    <div className={clsx(style.navbarContainer, "container")}>
      <div className={style.navbar}>
        <Button variant="link" href="/">
          <Image
            preload
            loading="eager"
            className={style.logo}
            width={90}
            height={20}
            src="logo.svg"
            alt=""
          />
        </Button>
        <Button
          className={style.menuButton}
          popoverTarget="menu"
          icon={HiMiniBars3}
          variant="link"
        />
        <nav className={style.menu} popover="auto" id="menu">
          {links.map(({ label, href }) => (
            <Button variant="link" href={href} key={label} role="listitem">
              {label}
            </Button>
          ))}
        </nav>
      </div>
    </div>
  );
}
