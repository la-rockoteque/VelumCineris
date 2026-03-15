import type { SVGProps } from "react";

export function RuneDivider(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 320 24" fill="none" aria-hidden="true" {...props}>
      <path d="M8 12H120" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M200 12H312" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path
        d="M160 3 166 9 175 12 166 15 160 21 154 15 145 12 154 9 160 3Z"
        fill="currentColor"
      />
    </svg>
  );
}
