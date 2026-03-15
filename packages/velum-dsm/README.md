# Velum DSM

Velum DSM is the reusable design-system source for Velum applications.

It is organized into four layers:

- `tokens/`: color, spacing, typography, motion, and semantic CSS variables
- `patterns/`: layout and workspace composition primitives
- `components/`: reusable UI controls built on the token contract
- `assets/`: code-based brand ornaments and marks

Usage in an app:

```tsx
import { VelumProvider, Button, Card } from "@velum/dsm";

export function AppShell() {
  return (
    <VelumProvider>
      <Card title="Velum">
        <Button>Launch</Button>
      </Card>
    </VelumProvider>
  );
}
```
