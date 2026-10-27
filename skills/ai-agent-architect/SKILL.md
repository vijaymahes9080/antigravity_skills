---
name: ai-agent-architect
description: Design and implement reliable autonomous AI agents, tool-calling reliability, ReAct reasoning loops, LangGraph state machines, multi-turn error recovery, and evaluation guardrails.
---

# AI Agent Architecture & Multi-Agent Orchestration

## 1. Intended Role & Domain
- **Primary Domain**: Artificial Intelligence & Agentic Systems
- **Target Roles**: AI Agent Developer, Multi-Agent Systems Engineer, Generative AI Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "build ai agent", "agentic workflow", "tool-calling reliability", "react loop", "langgraph", "multi-agent orchestration", "agent memory".
- **Contextual Inferences**: Projects building LLM applications with autonomous tool execution, complex state persistence, or agent swarms.
- **Chained Predecessors**: `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing simple single-shot text completion or deterministic prompt templates without tool-use or agency.
  - Training raw neural networks or deep learning model architectures from scratch.

## 4. Required Inputs & Context
- Agent objective, available tool definitions (JSON schemas), and environment constraints.
- LLM API provider or local inference engine (OpenAI, Gemini, Anthropic, Ollama).
- State persistence mechanism (PostgreSQL, Redis, SQLite).

## 5. Expected Outputs & Artifacts
- Finite state machine / agent graph definition (e.g. LangGraph / custom async engine).
- Strictly validated tool-calling schemas with error handling.
- Memory & context engineering pipeline with token budget enforcement.
- Automated evaluation suite assessing task completion and safety guardrails.

## 6. Step-by-Step Operating Procedure
1. **Agent State & Memory Design**:
   - Define immutable state dataclasses / TypedDict holding message history, scratchpad, and tool outputs.
2. **Tool Definition & Schema Contracts**:
   - Define tools with granular, descriptive docstrings and strict Pydantic/Zod schemas.
   - Restrict tool actions to atomic, idempotent operations where possible.
3. **Execution Loop & State Machine**:
   - Implement the ReAct cycle: Plan -> Reason -> Act -> Observe -> Reflect.
   - Enforce maximum iteration guards (`max_iterations = 10`) to prevent infinite looping.
4. **Error Interception & Recovery**:
   - Capture tool exceptions and feed structured error messages back to the model for self-correction.
5. **Guardrails & Evaluation**:
   - Run prompt injection checks, token budget monitors, and unit tests on tool invocation paths.

## 7. Repository Inspection & Planning Requirements
- Non-destructive package check:
  ```bash
  python -c "import langchain, langgraph, pydantic; print('Agent stack verified')" 2>/dev/null || echo "Custom agent stack"
  ```
- Preservation rule: Avoid unbounded agent loops; always require confirmation before mutating external production resources.

## 8. Tool & Dependency Requirements
- Python 3.10+ or Node.js 20+, Pydantic/Zod, LangGraph / custom state machine.

## 9. Implementation Guidelines & Best Practices
- Keep tool interfaces small: single responsibility per tool.
- Provide clear negative instructions in system prompts to deter agent hallucination of tool arguments.
- Use structured JSON outputs with schema validation for intermediate agent thoughts.

```python
from typing import TypedDict, Annotated, Sequence
import operator
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], operator.add]
    current_step: int
    is_complete: bool

class SearchToolArgs(BaseModel):
    query: str = Field(description="Search term without punctuation")
    max_results: int = Field(default=5, ge=1, le=20)

def search_tool(args: SearchToolArgs) -> dict:
    # Deterministic tool execution
    return {"results": [f"Result for {args.query}"]}
```

## 10. Error Handling & Recovery Procedures
- Tool argument schema validation error: Catch Pydantic `ValidationError` and prompt agent with exact parameter schema.
- Context window overflow: Summarize older conversational turns using a sliding-window compaction algorithm.

## 11. Security & Privacy Constraints
- Prevent prompt injection: Sanitize untrusted web content or tool outputs before injecting into model context.
- Never grant agents direct shell access with unrestricted root permissions; isolate in containers.

## 12. Verification & Testing Requirements
- Unit test tool dispatch:
  ```bash
  pytest tests/test_agent_tools.py -v
  ```
- Evaluate trajectory completion across a mock dataset of 10 representative user scenarios.

## 13. Completion Criteria
- Agent executes tool calls adhering strictly to schemas.
- Self-corrects on invalid inputs within 2 iterations.
- Terminates cleanly at `is_complete=True` or `max_iterations`.

## 14. Relevant Official References
- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., ICLR 2023).
- LangGraph Documentation (langchain-ai.github.io/langgraph/).
- Anthropic Tool Use & Agent Design Best Practices.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with modern tool-calling models (GPT-4o, Claude 3.5, Gemini 1.5/2.0).
