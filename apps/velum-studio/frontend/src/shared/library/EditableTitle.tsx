import { useMemo, useState } from "react";

interface EditableTitleProps {
  value: string;
  placeholder?: string;
  className?: string;
  editable?: boolean;
  onCommit: (next: string) => void;
}

export function EditableTitle(props: EditableTitleProps) {
  const [editing, setEditing] = useState(false);
  const display = useMemo(() => props.value || props.placeholder || "Untitled", [props.placeholder, props.value]);

  if (!props.editable) {
    return <h3 className={props.className}>{display}</h3>;
  }

  if (!editing) {
    return (
      <h3 className={props.className} onClick={() => setEditing(true)}>
        {display}
      </h3>
    );
  }

  return (
    <input
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

