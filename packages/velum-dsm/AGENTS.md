# Repository Guidelines

## Project Structure & Module Organization
`velum-dsm` is a TypeScript design-system package. Source lives in `src/`, with public exports routed through `src/index.ts`. The main layers are:

- `src/tokens/`: design tokens such as color, spacing, radius, motion, and typography scales
- `src/components/`: reusable UI components, usually one folder per component with `*.tsx`, `*.stories.tsx`, and `*.showcase.stories.tsx`
- `src/assets/`: branded visual assets and decorative components
- `src/patterns/`: Storybook MDX guidance for interaction and state patterns
- `src/provider/`: shared provider setup, including `VelumProvider`

Generated Storybook output is checked into `storybook-static/`; treat it as build output, not primary source.

## Build, Test, and Development Commands
- `asdf install`: install the repo's pinned tool versions before working locally
- `bun install`: install package dependencies
- `bun run storybook`: start Storybook on port `6006` using the repo-local home directory
- `bun run storybook:build`: create a static Storybook build
- `bun run typecheck`: run TypeScript validation with `tsc --noEmit`

Run commands from the package root: `packages/velum-dsm/`.

## Coding Style & Naming Conventions
Use TypeScript with React 18 and Styletron. Follow the existing file pattern: component folders use `PascalCase` names such as `src/components/Button/Button.tsx`, while support utilities under `_internal/` use `camelCase` names like `fieldStyles.ts`.

Prefer colocated stories for every exported token, asset, or component. Keep public exports centralized in barrel files such as `src/components/index.ts` and `src/index.ts`.

## Testing Guidelines
There is no standalone unit-test suite in this package yet. Minimum validation for changes is:

- `bun run typecheck`
- `bun run storybook` for local visual verification
- `bun run storybook:build` when changing Storybook config, stories, or docs

Preserve the existing story naming pattern: `Component.stories.tsx` and `Component.showcase.stories.tsx`.

## Commit & Pull Request Guidelines
Recent history uses short, imperative commit messages such as `Updated apps` and `Fixed json`. Keep commits brief, scoped, and action-oriented, for example `add toolbar story` or `fix text input state`.

Pull requests should summarize the change, list touched areas, include commands run, and attach screenshots when UI or Storybook output changes.

## Security & Configuration Tips
Do not commit secrets or machine-specific credentials. Keep local-only runtime artifacts in package-local folders such as `.storybook-home/`, and avoid hand-editing generated files under `storybook-static/` unless intentionally updating the build output.
