import { Client as Styletron } from "styletron-engine-atomic";
import { Provider, styled } from "styletron-react";

export const styletron = new Styletron();

export { Provider as StyletronProvider, styled };
