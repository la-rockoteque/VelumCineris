import { useCallback, useEffect, useMemo, useState } from "react";

export type ToastLevel = "success" | "warning" | "error" | "info";

export interface ToastItem {
  id: number;
  level: ToastLevel;
  message: string;
}

const TOAST_TIMEOUT_MS = 3600;

export function useToasts() {
  const [items, setItems] = useState<ToastItem[]>([]);

  const push = useCallback((message: string, level: ToastLevel = "info") => {
    const id = Date.now() + Math.floor(Math.random() * 1000);
    setItems((current) => [...current, { id, level, message }]);
    return id;
  }, []);

  const dismiss = useCallback((id: number) => {
    setItems((current) => current.filter((item) => item.id !== id));
  }, []);

  useEffect(() => {
    if (!items.length) {
      return;
    }

    const timers = items.map((item) =>
      window.setTimeout(() => {
        dismiss(item.id);
      }, TOAST_TIMEOUT_MS),
    );

    return () => {
      for (const timer of timers) {
        window.clearTimeout(timer);
      }
    };
  }, [dismiss, items]);

  return useMemo(
    () => ({
      items,
      push,
      dismiss,
    }),
    [dismiss, items, push],
  );
}
