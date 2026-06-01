# CLAUDE.md - Frontend Conventions

Svelte + Vite project. Read this alongside the root `CLAUDE.md`, which applies everywhere.

---

## Stack

- **Framework:** Svelte
- **Styling:** Scoped CSS in `.svelte` files with custom design tokens
- **Types:** TypeScript, strict mode
- **Design system:** Custom design tokens

---

## Component File Structure

Always use this order within a `.svelte` file (no exceptions):

```svelte
<script lang="ts">
  // 1. Imports
  // 2. Props (exported)
  // 3. Local state and derived values
  // 4. Functions and handlers
  // 5. Lifecycle
</script>

<!-- Template -->

<style>
  /* Styled components, ordered by visual hierarchy (outermost → innermost) */
</style>
```

---

## Naming

- **Component files:** PascalCase - `TimerDisplay.svelte`, `EventItem.svelte`
- **Non-component files:** camelCase - `timerStore.ts`, `formatTime.ts`
- **Folders:** camelCase - `compete/`, `ui/`, `eventList/`

---

## Folder Structure

```
src/
  lib/                  # Shared code only - imported via the $lib alias
    Navbar.svelte
    TwoColumnLayout.svelte
    types.ts
    fonts.css
    ...
  routes/
    +layout.svelte
    <route>/
      +page.svelte
      +page.server.ts
      ComponentA.svelte  # colocated - only used by this route
      componentUtils.ts
```

- **Route-specific components** live alongside the route files that use them, not in `lib/`.
- **`lib/` is for shared code only** - components or utilities used by more than one route or by the layout. Keep it flat; no subdirectories unless the shared surface grows large.
- When a route-specific component gets reused elsewhere, move it to `lib/`.
- There are no stores; use Svelte 5 `$state` classes or context instead.

---

## TypeScript

- **No `any`** - ever. Use `unknown` and narrow it, or define a proper type.
- All component props must be explicitly typed.
- **Props must use a named interface**, not an inline type literal. Define a `Props` interface (or a more specific name like `EventCardProps`) above the `$props()` call and reference it there.

```svelte
// ✅
interface Props {
  label: string;
  count: number;
}
const { label, count } = $props<Props>();

// ❌
const { label, count }: { label: string; count: number } = $props();
```

- Prefer `interface` for object shapes, `type` for unions and aliases.
- Export types from the file where they're defined; only centralize if shared across 3+ modules.

```ts
// ✅
interface EventItem {
  id: number
  name: string
  status: 'live' | 'done'
}

// ❌
const handleEvent = (data: any) => { ... }
```

---

## Styling

### Order within the style block

Order by **visual hierarchy** - outermost wrapper first, innermost last. Mirrors the template structure.

```svelte
<style>
  .competition-layout { ... }   /* outermost */
  .sidebar { ... }
  .week-header { ... }
  .event-list { ... }
  .event-item { ... }           /* innermost */
</style>
```

### Responsive styles - mobile-first

Write default styles for mobile, then override for desktop in a single `min-width` query at the **bottom** of the style block. Never use `max-width` queries.

```svelte
<style>
  /* default = mobile */
  .navbar { height: 3.25rem; }
  .nav-links { display: none; }

  /* desktop overrides */
  @media (min-width: 1024px) {
    .navbar { height: 4rem; }
    .nav-links { display: flex; }
  }
</style>
```

Apply section headers where appropriate. Use standard hyphens (`-`), not em- or en-h dashes.
Apply empty lines before and after section headers for readibility.

You may also use section headers for logical groups of related CSS classes; for example,
`.mobile-menu`, `.mobile-menu a`, `.mobile-menu a:hover`.

```svelte
<style>

  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .some-class { height: 10px; }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  .some-class { height: 25px; }

</style>
```

### Design tokens

Prefer tokens over raw values. Raw values are acceptable for genuine one-offs, but any value used more than once must use a token.

```svelte
<!-- ✅ -->
color: var(--color-text-primary);
border-radius: var(--border-radius-md);

<!-- ❌ -->
color: #1a1a1a;
border-radius: 6px;
```

---

## Component Extraction

Extract a new sub-component when a section of markup is **visually or functionally distinct** - even if used only once. Don't wait for reuse as the trigger.

Good signals to extract:
- It has its own internal state
- It maps to a clearly named UI concept (`ScrambleBar`, `EventItem`)
- Removing it from the parent makes the parent meaningfully easier to read

Keep inline only for simple, stateless fragments with no clear identity.

---

## Comments & Documentation

Every `.svelte` component must have a top-of-file `@component` docstring describing what it renders and any non-obvious behavior. Keep it to one or two sentences.

Use JSDoc only on complex or non-obvious logic - not on self-evident functions.

```ts
// ✅
/**
 * Computes the trimmed mean of solve times (drops best and worst).
 * Returns null if fewer than 3 valid (non-DNF) times are provided.
 */
function avgOfFive(times: (number | 'DNF')[]): number | null { ... }

// ❌
/** Sets the active event ID */
function setActiveEvent(id: number) {
  activeEventId = id
}
```