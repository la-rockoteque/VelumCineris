import type { ToastItem } from "app/useToasts";

interface ToastHostProps {
  items: ToastItem[];
  onDismiss: (id: number) => void;
}

export function ToastHost({ items, onDismiss }: ToastHostProps) {
  if (!items.length) {
    return null;
  }

  return (
    <div className="toast-host" aria-live="polite" aria-atomic="false">
      {items.map((item) => (
        <article key={item.id} className={`toast toast-${item.level}`.trim()}>
          <div className="toast-text">{item.message}</div>
          <button type="button" className="toast-close" onClick={() => onDismiss(item.id)}>
            ×
          </button>
        </article>
      ))}
    </div>
  );
}
