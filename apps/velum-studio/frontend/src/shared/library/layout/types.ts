import type { ReactNode } from "react";

export interface BlockProps {
  title?: string;
  subtitle?: string;
  className?: string;
  children: ReactNode;
}
