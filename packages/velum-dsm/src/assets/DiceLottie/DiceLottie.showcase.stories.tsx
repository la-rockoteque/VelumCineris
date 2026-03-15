import { useEffect, useRef } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Card, diceLottieUrl } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/DiceLottie",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function DiceLottiePreview(props: { size: number }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    let disposed = false;
    let player: { destroy?: () => void } | null = null;

    const mount = async () => {
      const canvas = canvasRef.current;
      if (!canvas) {
        return;
      }

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
    };

    void mount();

    return () => {
      disposed = true;
      player?.destroy?.();
    };
  }, []);

  return <canvas ref={canvasRef} style={{ width: `${props.size}px`, height: `${props.size}px`, display: "block" }} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <Card title="Dice Lottie Showcase" subtitle="Standardized references for loader usage at different scales.">
        <StateMatrix>
          <StateCase label="Tiny Loader" description="Inline status or badge-sized motion">
            <DiceLottiePreview size={18} />
          </StateCase>
          <StateCase label="Button Loader" description="Action feedback inside a button">
            <DiceLottiePreview size={24} />
          </StateCase>
          <StateCase label="Global Loader" description="Large wait-state animation for full-screen overlays">
            <DiceLottiePreview size={120} />
          </StateCase>
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
