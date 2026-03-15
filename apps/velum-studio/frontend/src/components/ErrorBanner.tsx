import { styled } from "app/styletron";
import { InlineButton } from "shared/library";

interface ErrorBannerProps {
  error: string;
  onClose: () => void;
}

const Banner = styled("div", {
  marginTop: "10px",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: "12px",
  border: "1px solid rgba(166, 53, 36, 0.4)",
  borderRadius: "10px",
  background: "rgba(248, 224, 218, 0.95)",
  color: "#7b2e20",
  padding: "10px 12px",
  fontSize: "0.86rem",
});

const Message = styled("span", {
  minWidth: 0,
});

export function ErrorBanner({ error, onClose }: ErrorBannerProps) {
  if (!error) {
    return null;
  }

  return (
    <Banner role="alert">
      <Message>{error}</Message>
      <InlineButton onClick={onClose} type="button">
        Dismiss
      </InlineButton>
    </Banner>
  );
}
