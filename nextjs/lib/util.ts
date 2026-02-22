export function trimStart(str: string, chars: string) {
  let i: number;
  for (i = 0; str.length > 0 && chars.includes(str[i]); i++);
  return str.slice(i);
}

export function trimEnd(str: string, chars: string) {
  let i: number;
  for (i = str.length - 1; i >= 0 && chars.includes(str[i]); i--);
  return str.slice(0, i + 1);
}

export function trim(str: string, chars: string) {
  return trimStart(trimEnd(str, chars), chars);
}
