import { QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";

import { VelumProvider } from "@velum/dsm";
import { queryClient } from "shared/query/client";
import App from "./App";
import "app/reset.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <VelumProvider>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </VelumProvider>
  </React.StrictMode>,
);
