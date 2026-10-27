---
name: multi-agent-orchestration
description: Multi-agent coordination topologies (hierarchical supervisor, swarm, peer-to-peer), LangGraph state graphs, AutoGen, CrewAI, inter-agent communication protocols, task delegation, and conflict resolution.
---

# Multi-Agent Orchestration & Distributed AI Topologies

## 1. Intended Role & Domain
- **Primary Domain**: Agentic AI & Orchestration
- **Target Roles**: Multi-Agent Systems Architect, AI Orchestration Engineer, Autonomous Systems Designer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "multi-agent system", "langgraph multi-agent", "agent swarm", "hierarchical supervisor", "autogen", "crewai", "inter-agent protocol", "agent delegation", "agent consensus", "collaborative agents".
- **Contextual Inferences**: Building systems where specialized agents (researcher, coder, reviewer, tester) collaborate, negotiate, and execute complex goals.
- **Chained Predecessors**: `ai-agent-architect`, `ai-rag-retrieval-engineering`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Designing a single isolated ReAct tool-calling loop -> use `/ai-agent-architect`.
  - Building straightforward deterministic workflow scripts -> use `/workflow-automation-scripting`.

## 4. Required Inputs & Context
- Agent personas and specialized domain capabilities (e.g. Architect, Engineer, QA Auditor).
- Orchestration topology preference:
  - **Hierarchical Supervisor**: Central router delegates tasks and evaluates sub-agent output.
  - **Network Swarm / Peer-to-Peer**: Agents pass state dynamically based on intent.
  - **Sequential Pipeline**: Fixed DAG with hand-offs and review gates.
- Shared state schema and message bus protocol.

## 5. Expected Outputs & Artifacts
- Multi-agent state machine (`orchestrator.py`) using LangGraph or typed state machines.
- Role specifications and isolated system prompts with strictly defined tool allowances.
- Guardrails against infinite deliberation loops and deadlock conditions.
- Execution trace logging and agent communication telemetry.

## 6. Step-by-Step Operating Procedure
1. **Topology & Coordination Selection**:
   - Choose topology: Hierarchical Supervisor for strict oversight; Swarm for collaborative discovery; Sequential DAG for deterministic pipelines.
2. **Shared State & Message Schema**:
   - Define immutable append-only message logs and structured task blackboard state.
3. **Agent Role & Tool Bound Isolation**:
   - Restrict tool sets per role: only the Coder has file-write tools; only the QA Auditor has test-runner tools.
4. **Handoff & Termination Protocol**:
   - Define unambiguous termination criteria (`FINAL_ANSWER`, `TASK_COMPLETE`, `ESCALATE_TO_HUMAN`).
   - Set maximum turn limits (e.g., max 15 turns) to prevent infinite inter-agent recursion.
5. **Conflict Resolution & Consensus Gate**:
   - Implement voting or supervisor evaluation when agents produce conflicting outputs.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of existing agent and LLM orchestrator files:
  ```bash
  grep -rnE "(StateGraph|LangGraph|autogen|crewai|AgentExecutor)" . 2>/dev/null
  ```
- Preservation rule: Always isolate subagent context windows to prevent token context explosion.

## 8. Tool & Dependency Requirements
- Python 3.11+, LangGraph >= 0.2.0, LangChain Core, Pydantic V2, asyncio.

## 9. Implementation Guidelines & Best Practices
- Robust hierarchical supervisor multi-agent system using LangGraph:

```python
import operator
from typing import Annotated, Sequence, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

# 1. Shared State Schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    next_step: str
    iteration_count: Annotated[int, operator.add]

# 2. Supervisor Router
class SupervisorDecision(BaseModel):
    next_worker: Literal["researcher", "coder", "reviewer", "FINISH"] = Field(
        description="The next specialized worker to invoke or FINISH if the goal is satisfied."
    )
    instruction: str = Field(description="Specific assignment for the chosen worker.")

def supervisor_node(state: AgentState):
    count = state.get("iteration_count", 0)
    if count >= 10:
        return {"next_step": "FINISH", "messages": ["[Supervisor] Max iteration threshold reached. Halting."], "iteration_count": 1}
    
    # In production, call LLM with structured output schema (SupervisorDecision)
    # Simulated routing logic:
    last_msg = state["messages"][-1] if state["messages"] else ""
    if "research" in last_msg.lower():
        return {"next_step": "coder", "messages": ["[Supervisor] Delegating to Coder."], "iteration_count": 1}
    elif "code" in last_msg.lower():
        return {"next_step": "reviewer", "messages": ["[Supervisor] Delegating to Reviewer."], "iteration_count": 1}
    elif "approved" in last_msg.lower():
        return {"next_step": "FINISH", "messages": ["[Supervisor] Goal satisfied."], "iteration_count": 1}
    else:
        return {"next_step": "researcher", "messages": ["[Supervisor] Delegating initial discovery to Researcher."], "iteration_count": 1}

def researcher_worker(state: AgentState):
    return {"messages": ["[Researcher] Completed background technical research on problem."], "iteration_count": 0}

def coder_worker(state: AgentState):
    return {"messages": ["[Coder] Wrote implementation code."], "iteration_count": 0}

def reviewer_worker(state: AgentState):
    return {"messages": ["[Reviewer] Code verified and approved."], "iteration_count": 0}

# 3. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("researcher", researcher_worker)
workflow.add_node("coder", coder_worker)
workflow.add_node("reviewer", reviewer_worker)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_step"],
    {
        "researcher": "researcher",
        "coder": "coder",
        "reviewer": "reviewer",
        "FINISH": END
    }
)

for worker in ["researcher", "coder", "reviewer"]:
    workflow.add_edge(worker, "supervisor")

orchestrator_app = workflow.compile()
```

## 10. Error Handling & Recovery Procedures
- Subagent failure or exception: Supervisor catches error, updates blackboard state, and routes to recovery agent.
- Infinite conversational ping-pong: Enforce strict step budget counter in the state machine; escalate to human if exceeded.

## 11. Security & Privacy Constraints
- Tool sandboxing: Execute code generation in isolated container sidecars with zero host file system access.
- Restrict sensitive environmental tokens from being broadcast to untrusted agent memory contexts.

## 12. Verification & Testing Requirements
- Multi-agent state graph terminates cleanly at `END` in 100% of test runs.
- Unit test individual agent nodes in isolation with mock state inputs.

## 13. Completion Criteria
- Distributed task completed with traceable agent contributions.
- Consensus reached and verified by reviewer agent.
- Total token consumption and execution latency logged.

## 14. Relevant Official References
- LangGraph Multi-Agent Architecture Documentation.
- AutoGen: Enabling Next-Gen LLM Applications (Wu et al., Microsoft Research).
- Communicative Agents for Software Development (ChatDev).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with LangGraph 0.2+, Pydantic V2, and modern asynchronous runtimes.
