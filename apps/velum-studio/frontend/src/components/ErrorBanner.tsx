interface ErrorBannerProps {
  error: string;
  onClose: () => void;
}

export function ErrorBanner({ error, onClose }: ErrorBannerProps) {
  if (!error) {
    return null;
  }

  return (
    <div className="error-banner" role="alert">
      <span>{error}</span>
      <button className="btn btn-inline" onClick={onClose} type="button">
        Dismiss
      </button>
    </div>
  );
}
