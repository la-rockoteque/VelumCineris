import { LoaderVisual } from "components/LoaderVisual";

interface LoadingOverlayProps {
  visible: boolean;
  message?: string;
}

export function LoadingOverlay({ visible, message = "Loading" }: LoadingOverlayProps) {
  return (
    <div className={`global-loading ${visible ? "" : "hidden"}`.trim()} role="status" aria-live="polite" aria-busy={visible}>
      <LoaderVisual sizeClass="loader-visual--global" />
      <div>{message}</div>
    </div>
  );
}
