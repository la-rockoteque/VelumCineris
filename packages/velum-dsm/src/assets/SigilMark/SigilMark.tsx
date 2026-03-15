import type { SVGProps } from "react";

export function SigilMark(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 120 120" fill="none" aria-hidden="true" {...props}>
      <circle cx="60" cy="60" r="54" stroke="currentColor" strokeWidth="4" />
      <path
        d="M60 20 78 42 102 48 84 70 88 98 60 84 32 98 36 70 18 48 42 42 60 20Z"
        stroke="currentColor"
        strokeWidth="4"
        strokeLinejoin="round"
      />
      <circle cx="60" cy="60" r="9" fill="currentColor" />
    </svg>
  );
}
