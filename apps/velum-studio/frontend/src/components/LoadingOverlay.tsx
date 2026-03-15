import { useEffect, useMemo, useState } from "react";
import { styled } from "app/styletron";
import { LoaderVisual } from "components/LoaderVisual";
import type { LoadingTriviaResponse } from "shared/types/api";

interface LoadingOverlayProps {
  visible: boolean;
  message?: string;
}

const ROTATE_INTERVAL_MS = 10_000;
const FALLBACK_TIDBITS = [
  "Did you know old maps of Orimond mark roads by seasonal dangers, not by distance.",
  "Did you know some spells in Orimond are named after failed experiments that became traditions.",
  "Did you know many monster epithets started as sailor warnings before becoming bestiary entries.",
];

const Overlay = styled("div", {
  position: "fixed",
  inset: "0",
  zIndex: 160,
  alignItems: "center",
  justifyContent: "center",
  flexDirection: "column",
  gap: "16px",
  background:
    "radial-gradient(circle at 20% 14%, rgba(127, 153, 102, 0.2), transparent 46%), radial-gradient(circle at 82% 80%, rgba(88, 117, 71, 0.16), transparent 42%), rgba(44, 34, 24, 0.34)",
  backdropFilter: "blur(5px)",
});

const RitualPanel = styled("div", {
  display: "grid",
  justifyItems: "center",
  gap: "10px",
  padding: "18px 22px",
  borderRadius: "14px",
  border: "1px solid rgba(126, 98, 67, 0.55)",
  background:
    "linear-gradient(155deg, rgba(245, 231, 207, 0.95) 0%, rgba(234, 215, 184, 0.94) 52%, rgba(222, 201, 166, 0.94) 100%)",
  boxShadow: "0 16px 36px rgba(21, 14, 8, 0.35), inset 0 0 0 1px rgba(147, 178, 117, 0.2)",
});

const Label = styled("div", {
  fontSize: "0.98rem",
  color: "#4b3b2a",
  textTransform: "uppercase",
  letterSpacing: "0.08em",
  fontWeight: 800,
  fontFamily: "\"Avenir Next Condensed\", \"Trebuchet MS\", serif",
});

const Flavor = styled("div", {
  fontSize: "0.72rem",
  color: "#5c6d4f",
  letterSpacing: "0.04em",
  textTransform: "uppercase",
  fontWeight: 700,
});

const Tidbit = styled("p", {
  margin: 0,
  maxWidth: "640px",
  textAlign: "center",
  fontSize: "0.92rem",
  lineHeight: 1.45,
  color: "#3f3428",
  fontStyle: "italic",
});

function pickRandomTidbit(pool: string[], previous: string): string {
  if (!pool.length) {
    return "";
  }
  if (pool.length === 1) {
    return pool[0];
  }

  let next = previous;
  for (let index = 0; index < 6; index += 1) {
    const candidate = pool[Math.floor(Math.random() * pool.length)];
    if (candidate && candidate !== previous) {
      next = candidate;
      break;
    }
  }
  return next === previous ? pool[0] : next;
}

export function LoadingOverlay({ visible, message = "Loading" }: LoadingOverlayProps) {
  const [loadedTidbits, setLoadedTidbits] = useState<string[]>([]);
  const [activeTidbit, setActiveTidbit] = useState<string>(() =>
    pickRandomTidbit(FALLBACK_TIDBITS, ""),
  );

  useEffect(() => {
    let canceled = false;

    const loadTidbits = async () => {
      try {
        const response = await fetch("/api/loading-trivia");
        if (!response.ok) {
          return;
        }
        const payload = (await response.json()) as LoadingTriviaResponse;
        const tidbits = payload.items
          .map((item) => (item.tidbit || "").trim())
          .filter((item) => item.length > 0);
        if (!canceled && tidbits.length) {
          setLoadedTidbits(tidbits);
        }
      } catch {
        // Keep local fallback tidbits if API lookup fails.
      }
    };

    void loadTidbits();
    return () => {
      canceled = true;
    };
  }, []);

  const triviaPool = useMemo(
    () => (loadedTidbits.length ? loadedTidbits : FALLBACK_TIDBITS),
    [loadedTidbits],
  );

  useEffect(() => {
    if (!visible) {
      return;
    }
    setActiveTidbit((current) => pickRandomTidbit(triviaPool, current));
    const timer = window.setInterval(() => {
      setActiveTidbit((current) => pickRandomTidbit(triviaPool, current));
    }, ROTATE_INTERVAL_MS);
    return () => {
      window.clearInterval(timer);
    };
  }, [visible, triviaPool]);

  const display = visible ? "flex" : "none";

  return (
    <Overlay role="status" aria-live="polite" aria-busy={visible} style={{ display }}>
      <RitualPanel>
        <LoaderVisual sizeClass="loader-visual--global" />
        <Label>{message}</Label>
        <Flavor>Consulting The Codex</Flavor>
        <Tidbit>{activeTidbit}</Tidbit>
      </RitualPanel>
    </Overlay>
  );
}
