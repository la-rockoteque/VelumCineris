import loaderOrb from "../../assets/loader-cute-orb.svg";

interface LoaderVisualProps {
  sizeClass?: "loader-visual--tiny" | "loader-visual--small" | "loader-visual--button" | "loader-visual--table" | "loader-visual--global";
}

export function LoaderVisual({ sizeClass = "loader-visual--small" }: LoaderVisualProps) {
  return (
    <span className={`loader-visual ${sizeClass}`.trim()} aria-hidden="true">
      <img className="loader-image" src={loaderOrb} alt="" loading="lazy" />
      <span className="loader-fallback" />
    </span>
  );
}
