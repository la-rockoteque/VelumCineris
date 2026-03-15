import { useEffect, useRef, useState } from "react";
import { styled } from "app/styletron";
import diceLottieUrl from "../../assets/dice.lottie?url";

interface LoaderVisualProps {
  sizeClass?: "loader-visual--tiny" | "loader-visual--small" | "loader-visual--button" | "loader-visual--table" | "loader-visual--global";
}

const SIZE_STYLES: Record<NonNullable<LoaderVisualProps["sizeClass"]>, { width: string; height: string }> = {
  "loader-visual--tiny": { width: "14px", height: "14px" },
  "loader-visual--small": { width: "18px", height: "18px" },
  "loader-visual--button": { width: "18px", height: "18px" },
  "loader-visual--table": { width: "56px", height: "56px" },
  "loader-visual--global": { width: "190px", height: "190px" },
};

const Root = styled("span", ({ $size }: { $size: NonNullable<LoaderVisualProps["sizeClass"]> }) => ({
  position: "relative",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  ...SIZE_STYLES[$size],
}));

const Canvas = styled("canvas", ({ $size }: { $size: NonNullable<LoaderVisualProps["sizeClass"]> }) => ({
  width: SIZE_STYLES[$size].width,
  height: SIZE_STYLES[$size].height,
  display: "block",
}));

const spinAnimation = {
  from: {
    transform: "rotate(0deg)",
  },
  to: {
    transform: "rotate(360deg)",
  },
};

const Fallback = styled("span", {
  position: "absolute",
  inset: 0,
  borderRadius: "50%",
  border: "2px solid rgba(87, 67, 46, 0.42)",
  borderTopColor: "rgba(120, 95, 68, 0.82)",
  animationName: spinAnimation,
  animationDuration: "900ms",
  animationTimingFunction: "linear",
  animationIterationCount: "infinite",
});

export function LoaderVisual({ sizeClass = "loader-visual--small" }: LoaderVisualProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let disposed = false;
    let player: { destroy?: () => void } | null = null;

    const mount = async () => {
      const canvas = canvasRef.current;
      if (!canvas) {
        return;
      }
      try {
        const module = await import("@lottiefiles/dotlottie-web");
        if (disposed) {
          return;
        }
        const DotLottie = module.DotLottie as new (config: {
          canvas: HTMLCanvasElement;
          src: string;
          autoplay: boolean;
          loop: boolean;
        }) => { destroy?: () => void };
        player = new DotLottie({
          canvas,
          src: diceLottieUrl,
          autoplay: true,
          loop: true,
        });
        if (!disposed) {
          setReady(true);
        }
      } catch {
        if (!disposed) {
          setReady(false);
        }
      }
    };

    void mount();

    return () => {
      disposed = true;
      player?.destroy?.();
    };
  }, []);

  return (
    <Root $size={sizeClass} aria-hidden="true">
      <Canvas ref={canvasRef} $size={sizeClass} />
      {!ready && <Fallback />}
    </Root>
  );
}
