# DeepSeek SuperAgent: Safety and Authorization Reference

This reference details the security invariants, gate admission policies, and human approval checkpoints that govern all autonomous actions.

---

## 1. Safety Invariants (Non-Negotiable)

1. **No Silent Destructive Actions**: Any deletion of directories, database data, or configuration requires explicit confirmation.
2. **Credential Immutability**: The agent MUST NEVER expose, print, log, or overwrite API keys, SSH keys, certificates, or `.env` files.
3. **Bounded Autonomous Retries**: When commands or tests fail, the worker may attempt at most 3 internal remediation cycles before reporting `blocked` or `failed`. Infinite loops are strictly prohibited.
4. **No Security Sandbox Evasion**: The agent must not attempt to circumvent network proxies, file access restrictions, or process boundaries.
5. **Human Attention Economy**: Never prompt the user for routine decisions (e.g., variable names, minor file paths). Only interrupt for true decision forks or safety checkpoints.

---

## 2. Mandatory Approval Checkpoint Matrix

The following matrix defines the operations requiring human approval and the required format:

| Category | High-Risk Operation | Agent Behavior | Approval Question Format |
| :--- | :--- | :--- | :--- |
| **File System** | Deleting non-temporary files or directories | Pause execution; do not run delete command | *"I need to delete `<path>` because `<reason>`. Should I proceed?"* |
| **Credentials** | Modifying `.env`, secrets manager, or tokens | Halt; require operator to supply or edit | *"Changing `<secret_name>` requires your manual action or approval. Please confirm or provide updated value."* |
| **Dependencies** | Adding unvetted external dependencies or build plugins | Justify need; check package provenance | *"To implement `<feature>`, I propose adding dependency `<pkg>@<ver>`. Do you approve this addition?"* |
| **Database** | Running destructive schema migrations (`DROP`, `TRUNCATE`) | Generate migration script; pause execution | *"Migration `<name>` drops column/table `<target>`. Do you approve running this migration?"* |
| **Git Operations** | `git push --force`, deleting branches, hard resets | Refuse force-pushes; ask before destructive resets | *"A force-push or hard reset to `<branch>` will overwrite commit history. Do you approve this operation?"* |
| **Infrastructure** | Modifying production terraform, k8s, or cloud resources | Produce diff; request explicit sign-off | *"Infrastructure configuration in `<manifest>` modifies production resources. Please review diff and approve."* |
| **Deployment** | Auto-merging to `main` or deploying to live stages | Enforce approval gate | *"All tests pass and diff is clean. Do you approve merging PR #`<num>` to `main`?"* |

---

## 3. Auto-Merge & Delivery Rules

Derived from DeepSeek SuperAgent's delivery constraints:
- **Default Policy**: The agent account NEVER merges its own pull requests directly unless explicitly authorized.
- **Threshold Rule**: Proactive auto-merge is permitted ONLY IF:
  1. All automated CI checks and regression tests have passed with 100% green status.
  2. The net change is strictly under **200 lines of code** (additions + deletions).
  3. No public API signatures or database schemas are altered.
  4. An authorized team member has approved the review thread.
- If any condition is unmet, the pull request remains open for human review.

---

## 4. Handback Protocol

When an assigned worker discovers:
1. The request asks for work beyond the assigned mandate scope.
2. A required architecture direction is open or ambiguous.
3. The thread or issue is unrelated to the worker's component.

The worker MUST NOT guess or expand scope. It executes a formal handback:
- Set status to `blocked` or `dropped`.
- Output a single-sentence rationale: *"Handback: `<reason>` (e.g. requires cross-service schema redesign outside mandate)."*
- Orchestrator routes the item back to the user or creates a new ticket.
