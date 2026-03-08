import { createContext, useContext } from "react";
import type { ReactNode } from "react";

import type { SelectedRow } from "shared/types/api";
import { pickItemName } from "shared/utils/fields";

export interface CurrentSheetContextValue {
  source: string;
  sheet: string;
}

export interface CurrentItemContextValue {
  selected: SelectedRow | null;
  name: string;
}

const CurrentSheetContext = createContext<CurrentSheetContextValue>({
  source: "auto",
  sheet: "",
});

const CurrentItemContext = createContext<CurrentItemContextValue>({
  selected: null,
  name: "",
});

interface CurrentSheetProviderProps {
  value: CurrentSheetContextValue;
  children: ReactNode;
}

interface CurrentItemProviderProps {
  value: SelectedRow | null;
  children: ReactNode;
}

export function CurrentSheetProvider(props: CurrentSheetProviderProps) {
  return <CurrentSheetContext.Provider value={props.value}>{props.children}</CurrentSheetContext.Provider>;
}

export function CurrentItemProvider(props: CurrentItemProviderProps) {
  const selected = props.value;
  const name = selected ? pickItemName(selected.rowData) : "";
  return <CurrentItemContext.Provider value={{ selected, name }}>{props.children}</CurrentItemContext.Provider>;
}

export function useCurrentSheet() {
  return useContext(CurrentSheetContext);
}

export function useCurrentItem() {
  return useContext(CurrentItemContext);
}
