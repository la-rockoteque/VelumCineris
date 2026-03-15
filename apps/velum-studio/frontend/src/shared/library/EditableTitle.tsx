import { useMemo, useState } from "react";
import { styled } from "app/styletron";


interface EditableTitleProps {
  value: string;
  placeholder?: string;
  editable?: boolean;
  onCommit: (next: string) => void;
}

const Title = styled("h3", ({ $editable }: { $editable: boolean }) => ({
  margin: 0,
  ...( $editable
    ? {
        cursor: "pointer",
        ":hover": {
          color: "var(--accent)",
        },
      }
    : {}),
}));

const TitleInput = styled("input", {
  fontSize: "1.2rem",
  fontFamily: "\"Avenir Next Condensed\", \"Trebuchet MS\", sans-serif",
  letterSpacing: "0.03em",
  textTransform: "uppercase",
});

export function EditableTitle(props: EditableTitleProps) {
  const [editing, setEditing] = useState(false);
  const display = useMemo(() => props.value || props.placeholder || "Untitled", [props.placeholder, props.value]);

  if (!props.editable) {
    return <Title $editable={false}>{display}</Title>;
  }

  if (!editing) {
    return (
      <Title $editable onClick={() => setEditing(true)}>
        {display}
      </Title>
    );
  }

  return (
    <TitleInput
      autoFocus
      defaultValue={props.value}
      onBlur={(event) => {
        props.onCommit(event.target.value.trim());
        setEditing(false);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          props.onCommit((event.target as HTMLInputElement).value.trim());
          setEditing(false);
        }
        if (event.key === "Escape") {
          setEditing(false);
        }
      }}
    />
  );
}
