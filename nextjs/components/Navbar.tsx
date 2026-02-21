import Image from "next/image";
import style from "./Navbar.module.css";

type NavbarProps = {};

export function Navbar() {
  return (
    <div className={style.navbar}>
      <Image width={130} height={40} src="logo.svg" alt="" />
    </div>
  );
}
