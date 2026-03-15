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

export const brandAssets = {
  marks: ["SigilMark", "RuneDivider", "CornerFlourish"],
  tone: "parchment-ember-moss",
} as const;
