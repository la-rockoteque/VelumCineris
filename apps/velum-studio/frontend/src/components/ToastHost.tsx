import type { ToastItem } from "app/useToasts";
import { styled } from "app/styletron";

interface ToastHostProps {
  items: ToastItem[];
  onDismiss: (id: number) => void;
}

const Host = styled("div", {
  position: "fixed",
  right: "16px",
  bottom: "14px",
  zIndex: 120,
  display: "grid",
  gap: "8px",
  width: "min(360px, calc(100vw - 24px))",
  pointerEvents: "none",
});

const levelBorders: Record<ToastItem["level"], string> = {
  success: "rgba(43, 122, 63, 0.35)",
  warning: "rgba(154, 107, 24, 0.4)",
  info: "rgba(47, 96, 112, 0.42)",
  error: "rgba(166, 53, 36, 0.45)",
};

const toastInAnimation = {
  from: {
    opacity: 0,
    transform: "translateY(8px)",
  },
  to: {
    opacity: 1,
    transform: "translateY(0)",
  },
};

const Toast = styled("article", {
  pointerEvents: "auto",
  borderRadius: "10px",
  border: "1px solid var(--border)",
  background: "rgba(255, 250, 240, 0.98)",
  boxShadow: "0 10px 24px rgba(0, 0, 0, 0.14)",
  padding: "10px 12px",
  display: "grid",
  gridTemplateColumns: "minmax(0, 1fr) auto",
  gap: "8px",
  alignItems: "start",
  animationName: toastInAnimation,
  animationDuration: "180ms",
  animationTimingFunction: "ease-out",
});

const ToastText = styled("div", {
  fontSize: "0.82rem",
  color: "#4f4638",
});

const CloseButton = styled("button", {
  border: "0",
  background: "transparent",
  color: "#73685a",
  fontSize: "0.82rem",
  fontWeight: 700,
  cursor: "pointer",
  lineHeight: 1,
  padding: "2px 4px",
});

export function ToastHost({ items, onDismiss }: ToastHostProps) {
  if (!items.length) {
    return null;
  }

  return (
    <Host aria-live="polite" aria-atomic="false">
      {items.map((item) => (
        <Toast key={item.id} style={{ borderColor: levelBorders[item.level] }}>
          <ToastText>{item.message}</ToastText>
          <CloseButton type="button" onClick={() => onDismiss(item.id)}>
            ×
          </CloseButton>
        </Toast>
      ))}
    </Host>
  );
}
