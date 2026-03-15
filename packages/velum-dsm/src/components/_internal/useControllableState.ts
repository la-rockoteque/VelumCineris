import { useEffect, useState } from "react";

export function useControllableState<T>(value: T | undefined, fallback: T) {
  const [internalValue, setInternalValue] = useState<T>(value ?? fallback);

  useEffect(() => {
    if (value !== undefined) {
      setInternalValue(value);
    }
  }, [value]);

  return [internalValue, setInternalValue] as const;
}
