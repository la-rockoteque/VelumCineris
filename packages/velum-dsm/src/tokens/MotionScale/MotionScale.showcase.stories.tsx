import type { Meta, StoryObj } from "@storybook/react";

import { motionScale } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/MotionScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

const bar = (duration: string) => ({
  width: "120px",
  height: "12px",
  borderRadius: "999px",
  background: "linear-gradient(90deg, var(--accent-soft), var(--accent))",
  animation: `pulse ${duration} infinite alternate`,
});

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <style>{`@keyframes pulse { from { transform: scaleX(0.55); opacity: 0.5; } to { transform: scaleX(1); opacity: 1; } }`}</style>
      <StateMatrix>
        <StateCase label="Quick" description={motionScale.quick}>
          <div style={bar(motionScale.quick)} />
        </StateCase>
        <StateCase label="Base" description={motionScale.base}>
          <div style={bar(motionScale.base)} />
        </StateCase>
        <StateCase label="Slow" description={motionScale.slow}>
          <div style={bar(motionScale.slow)} />
        </StateCase>
        <StateCase label="Easing" description={JSON.stringify(motionScale.easing)} minHeight="96px">
          <div style={{ fontFamily: "var(--velum-font-mono)", fontSize: "0.82rem" }}>{JSON.stringify(motionScale.easing)}</div>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
