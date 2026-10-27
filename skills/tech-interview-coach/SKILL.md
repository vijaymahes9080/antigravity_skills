---
name: tech-interview-coach
description: Comprehensive technical interview preparation covering Data Structures & Algorithms (DSA), System Design tradeoffs, Behavioral interview mastery with the STAR method, and live coding assessment drills.
---

# Technical Interview & Coding Assessment Coaching

## 1. Intended Role & Domain
- **Primary Domain**: Career & Professional Development
- **Target Roles**: Technical Interview Coach, Coding Assessment Coach, Senior Engineering Mentor
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "technical interview prep", "mock interview", "leetcode coach", "system design interview", "behavioral star method", "coding assessment practice", "staff engineer interview".
- **Contextual Inferences**: Candidates preparing for technical screening, live pair-programming, or system design loops at technology companies.
- **Chained Predecessors**: `ats-resume-optimizer`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Factual production bug debugging in an active enterprise repository.
  - Generating cheat sheets designed for unauthorized cheating during live exams.

## 4. Required Inputs & Context
- Target role level (Junior, Mid, Senior, Staff/Principal Engineer).
- Focus area: DSA / Coding, System Design, or Behavioral / Leadership.
- Target company archetype (Big Tech, High-Growth Startup, Enterprise).

## 5. Expected Outputs & Artifacts
- Step-by-step problem breakdown following the UMPIRE method (Understand, Match, Plan, Implement, Review, Evaluate).
- Optimal algorithm implementation with explicit Time and Space Big-O complexity analysis.
- System Design Architecture blueprint with capacity estimations and tradeoff justifications.
- STAR behavioral answer scripts (Situation, Task, Action, Result).

## 6. Step-by-Step Operating Procedure
1. **Assessment & Diagnostic Baseline**:
   - Assess candidate's baseline across three pillars: Problem-Solving (DSA), Architecture (System Design), and Communication (Behavioral).
2. **DSA Coaching (The UMPIRE Method)**:
   - **Understand**: Clarify inputs, edge cases (null, empty, negative, duplicates), and constraints.
   - **Match**: Associate problem pattern (Two Pointers, Sliding Window, Monotonic Stack, BFS/DFS, TopoSort, Dynamic Programming).
   - **Plan**: Outline approach in English pseudocode before touching syntax.
   - **Implement**: Write clean, modular, bug-free code.
   - **Review**: Dry-run with a concrete example step-by-step.
   - **Evaluate**: State exact Big-O time and space complexity.
3. **System Design Coaching (The 4-Step Framework)**:
   - Step 1: Scope & Functional/Non-Functional Requirements (QPS, storage, latency).
   - Step 2: High-Level Architecture & API Design (Endpoints, Data Models).
   - Step 3: Deep Dive into Bottlenecks (Sharding, Caching, Replication, Consistency).
   - Step 4: Failure Modes & Tradeoffs (CAP theorem, split-brain, network partitions).
4. **Behavioral STAR Coaching**:
   - Structure narratives into concise 2-minute answers: Situation (15%), Task (15%), Action (50%), Result (20%).
5. **Interactive Feedback & Scorecard**:
   - Provide constructive scoring across technical competence, communication, and problem decomposition.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection: Read candidate code samples or problem statements.
- Preservation rule: Encourage reasoning aloud; do not jump straight to the optimal solution without exploring naive brute-force baselines.

## 8. Tool & Dependency Requirements
- Markdown generation, Python / TypeScript / Java execution environment for verifying algorithmic solutions.

## 9. Implementation Guidelines & Best Practices
- Focus on patterns, not memorizing 500 individual LeetCode questions:
  - Slidng Window -> Subarray/substring contiguous bounds.
  - Fast & Slow Pointers -> Cycle detection, middle of linked list.
  - Monotonic Queue/Stack -> Next greater element, histogram areas.
  - Breadth-First Search -> Shortest unweighted paths, level-order traversal.

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find maximum value in each sliding window of size k.
    Time Complexity: O(N) - each element pushed and popped at most once.
    Space Complexity: O(K) - deque stores at most k indices.
    """
    from collections import deque
    
    dq = deque() # Stores indices of monotonically decreasing elements
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside current window [i - k + 1, i]
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # Maintain monotonically decreasing order in deque
        while dq and nums[dq[-1]] < num:
            dq.pop()
            
        dq.append(i)
        
        # Append to result once first full window is reached
        if i >= k - 1:
            result.append(nums[dq[0]])
            
    return result
```

## 10. Error Handling & Recovery Procedures
- Candidate gets stuck during problem solving: Provide progressive Socratic hints (e.g. "What data structure allows O(1) minimum lookups?" or "Notice the array is sorted").

## 11. Security & Privacy Constraints
- Maintain candidate confidentiality regarding company names and interview timeline details.

## 12. Verification & Testing Requirements
- Unit test algorithm solutions against edge cases:
  ```python
  assert max_sliding_window([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
  assert max_sliding_window([1], 1) == [1]
  assert max_sliding_window([1,-1], 1) == [1, -1]
  ```

## 13. Completion Criteria
- Optimal solution implemented and verified with automated test assertions.
- Time and Space complexity accurately analyzed.
- Tradeoffs explained clearly.

## 14. Relevant Official References
- "Cracking the Coding Interview" (Gayle Laakmann McDowell).
- "Designing Data-Intensive Applications" (Martin Kleppmann).
- System Design Primer (Donne Martin).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Aligned with current FAANG/MAMAA and tier-1 startup interview bars.
