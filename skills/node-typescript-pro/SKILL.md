---
name: node-typescript-pro
description: Modern Node.js 22+ and TypeScript 5+ full-stack and backend engineering, native ESM modules, strict type-safety, Vitest unit testing, and high-performance async workflows.
---

# Modern Node.js & TypeScript Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Software Development & Full-Stack Engineering
- **Target Roles**: Node.js Developer, TypeScript Developer, Full-Stack Developer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "node.js", "typescript", "modern node", "vitest", "fastify", "express typescript", "strict typescript".
- **Contextual Inferences**: Repositories containing `package.json`, `tsconfig.json`, `.ts` files.
- **Chained Predecessors**: `task-decomposition`, `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Python, Go, Java or pure non-JS backend projects.
  - Browser-only CSS/HTML tasks with no Node.js runtime.

## 4. Required Inputs & Context
- Node.js runtime (v20+ LTS, preferred Node 22+).
- `package.json` with `"type": "module"`.
- `tsconfig.json` with `"strict": true`.

## 5. Expected Outputs & Artifacts
- Strongly typed TypeScript modules using ES Modules (`import`/`export`).
- High-performance API handlers (Fastify or Express) with input validation (Zod).
- Automated unit test suite using Vitest or Node Test Runner (`node:test`).

## 6. Step-by-Step Operating Procedure
1. **Runtime & Module Configuration**:
   - Verify Node version: `node -v` and ensure `"type": "module"` in `package.json`.
   - Ensure `tsconfig.json` specifies `"target": "ES2022"`, `"moduleResolution": "NodeNext"`.
2. **Schema & Contract Definition**:
   - Define domain schemas and runtime validation using Zod (`z.infer<typeof Schema>`).
3. **Async Architecture & Stream Handling**:
   - Utilize native `fetch`, `node:stream`, `node:fs/promises`, and `AbortController` for cancellable async I/O.
4. **Service & Controller Assembly**:
   - Organize controllers, services, and repositories with dependency injection.
5. **Testing & Linting**:
   - Execute test runner with coverage and run type-checker (`tsc --noEmit`).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection commands:
  ```bash
  node -v && npm -v
  cat package.json | grep -E "(dependencies|devDependencies)" -A 10
  npx tsc --version
  ```
- Preservation rule: Do not downgrade strict mode in `tsconfig.json` to silence type errors; fix types properly.

## 8. Tool & Dependency Requirements
- Node.js 20+, npm/pnpm/yarn, TypeScript 5.x, Vitest or Jest.

## 9. Implementation Guidelines & Best Practices
- Never use `any`; use `unknown` with runtime type narrowing or Zod schemas.
- Avoid unhandled promise rejections: always await or return promises.
- Use native `node:` prefix for built-in modules (`node:path`, `node:fs`, `node:crypto`).

```typescript
import { z } from 'zod';
import { type Request, type Response } from 'express';

export const UserCreateSchema = z.object({
  username: z.string().min(3).max(30),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
});

export type UserCreateInput = z.infer<typeof UserCreateSchema>;

export async function createUserHandler(req: Request, res: Response): Promise<void> {
  const result = UserCreateSchema.safeParse(req.body);
  if (!result.success) {
    res.status(400).json({ error: 'Validation failed', details: result.error.format() });
    return;
  }
  const user = await userService.create(result.data);
  res.status(201).json(user);
}
```

## 10. Error Handling & Recovery Procedures
- `ERR_REQUIRE_ESM`: Ensure import paths include `.js` extensions when `"moduleResolution": "NodeNext"` is active.
- Unhandled rejection crashes: Ensure top-level `process.on('unhandledRejection')` logs stack trace before graceful exit.

## 11. Security & Privacy Constraints
- Prevent Prototype Pollution: Validate JSON input keys and avoid recursive object merges without `Object.hasOwn()`.
- Mitigate ReDoS: Avoid high-complexity regular expressions on untrusted input; use Zod or re2.

## 12. Verification & Testing Requirements
- Type check:
  ```bash
  npx tsc --noEmit
  ```
- Run Vitest / Node test runner:
  ```bash
  npx vitest run || npm test
  ```

## 13. Completion Criteria
- Zero TypeScript compiler errors (`tsc --noEmit` exits 0).
- Zero lint errors.
- 100% passing tests in Vitest suite.

## 14. Relevant Official References
- TypeScript Official Handbook (typescriptlang.org).
- Node.js Official Documentation (nodejs.org).
- Zod Documentation (zod.dev).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Node.js 20, 22 LTS, and TypeScript 5.5+.
