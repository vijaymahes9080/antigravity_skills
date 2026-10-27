---
name: react-nextjs-pro
description: Modern React 19 and Next.js 15 App Router architecture, React Server Components (RSC), Server Actions, TanStack Query, optimistic UI updates, streaming SSR, and edge performance.
---

# React 19 & Next.js 15 App Router Architecture

## 1. Intended Role & Domain
- **Primary Domain**: Web Engineering & Frontend Architecture
- **Target Roles**: Frontend Developer, React Developer, Full-Stack Web Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "react", "next.js", "nextjs 15", "react server components", "rsc", "server actions", "tanstack query", "app router".
- **Contextual Inferences**: Repositories containing `next.config.js`, `next.config.mjs`, `app/` directory, React 18/19 dependencies.
- **Chained Predecessors**: `task-decomposition`, `design-systems-engineer`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Mobile Flutter or native Swift/Kotlin applications.
  - Legacy jQuery or AngularJS 1.x without React.

## 4. Required Inputs & Context
- Node.js 18.18+ or 20/22+.
- Next.js 14/15 App Router project structure (`app/layout.tsx`, `app/page.tsx`).
- Component wireframes or user interface specifications.

## 5. Expected Outputs & Artifacts
- Composable React Server Components (`async` components) for data fetching.
- Interactive Client Components (`'use client'`) isolated to interactive boundaries.
- Secure Server Actions (`'use server'`) for mutating backend data.
- Responsive, accessible page views with loading skeletons and error boundaries.

## 6. Step-by-Step Operating Procedure
1. **Server vs Client Boundary Decomposition**:
   - Keep data fetching, database queries, and secret-dependent operations in Server Components.
   - Restrict `'use client'` to leaf components requiring browser event listeners (`onClick`, `useState`, `useEffect`).
2. **Server Actions & Mutations**:
   - Implement mutations in `actions/` using `'use server'` with input validation via Zod.
   - Use `revalidatePath()` or `revalidateTag()` for cache invalidation.
3. **Streaming & Suspense Boundaries**:
   - Wrap slow asynchronous data fetches in `<Suspense fallback={<Skeleton />}>` to enable incremental streaming.
4. **Client State & Optimistic Updates**:
   - Use React 19's `useOptimistic` hook for instant UI feedback before network confirmation.
5. **SEO & Metadata**:
   - Export dynamic `generateMetadata()` for OpenGraph and search engine optimization.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of Next.js setup:
  ```bash
  cat package.json | grep -E "(next|react|react-dom)" -A 3
  ls app/ 2>/dev/null || ls src/app/ 2>/dev/null
  ```
- Preservation rule: Never import server-only packages (e.g. database clients, secret keys) into Client Components marked with `'use client'`.

## 8. Tool & Dependency Requirements
- Next.js 14/15, React 19, TypeScript 5+, Tailwind CSS or Vanilla CSS Modules, Zod.

## 9. Implementation Guidelines & Best Practices
- Never waterfall async requests in Server Components; fetch parallel resources with `Promise.all()`.
- Use the `server-only` package (`import 'server-only'`) in utility files containing database queries to prevent accidental leakage into client bundles.

```tsx
import { Suspense } from 'react';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

// Server Action
export async function updateItemAction(formData: FormData) {
  'use server';
  const name = formData.get('name') as string;
  await db.item.update({ where: { id: 1 }, data: { name } });
  revalidatePath('/dashboard');
}

// Server Component
export default async function DashboardPage() {
  const dataPromise = db.item.findMany();

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <Suspense fallback={<div className="animate-pulse h-32 bg-gray-200 rounded" />}>
        <ItemList dataPromise={dataPromise} />
      </Suspense>
    </main>
  );
}
```

## 10. Error Handling & Recovery Procedures
- `Hydration failed because the initial UI does not match the server`: Eliminate client-side-only values (e.g. `window.innerWidth`, `Date.now()`, random numbers) from the initial render pass.
- Server action unhandled rejection: Wrap mutations in try-catch and return structured `{ success: false, error: message }` objects.

## 11. Security & Privacy Constraints
- Never expose environment variables without the `NEXT_PUBLIC_` prefix to the client.
- Always authenticate user sessions inside Server Actions before executing database mutations.

## 12. Verification & Testing Requirements
- Type check and build:
  ```bash
  npm run build
  ```
- Run component tests:
  ```bash
  npm test || npx vitest run
  ```

## 13. Completion Criteria
- Next.js production build succeeds with clean page routes (`○ Static` / `ƒ Dynamic`).
- Zero hydration errors in browser console.
- Streaming Suspense skeletons function smoothly.

## 14. Relevant Official References
- Next.js App Router Documentation (nextjs.org/docs/app).
- React 19 Documentation & Server Components Guide (react.dev).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Next.js 15+ and React 19.
