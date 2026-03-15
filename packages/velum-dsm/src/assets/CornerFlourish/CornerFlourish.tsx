import type { SVGProps } from "react";

export function CornerFlourish(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 56 56" fill="none" aria-hidden="true" {...props}>
      <path
        d="M6 50C12 30 24 18 50 6M21 50H6V35M50 21V6H35"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
