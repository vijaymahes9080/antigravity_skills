---
name: local-llm-integration
description: Integrate, serve, and benchmark local open-weight language models using Ollama, vLLM, and llama.cpp. Master GGUF quantization, hardware acceleration, streaming responses, and OpenAI-compatible API adapters.
---

# Local LLM Integration & Self-Hosted Inference

## 1. Intended Role & Domain
- **Primary Domain**: Artificial Intelligence & Infrastructure
- **Target Roles**: Local LLM Integration Engineer, Edge AI Engineer, AI Infrastructure Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "local llm", "ollama", "vllm", "llama.cpp", "gguf quantization", "offline ai model", "run mistral locally", "run llama 3 locally".
- **Contextual Inferences**: Air-gapped environments, zero-cloud data privacy mandates, cost-constrained offline inference.
- **Chained Predecessors**: `ai-agent-architect`, `ai-rag-retrieval-engineering`.

## 3. Explicit Exclusions
- Do NOT use when:
  - User strictly specifies managed proprietary cloud APIs (OpenAI, Gemini, Anthropic) without any local hosting requirement.
  - Client devices lack sufficient RAM/VRAM to load minimal quantized models (< 4GB available).

## 4. Required Inputs & Context
- Target open-weight model (e.g. Llama 3.1 8B, Mistral 7B, Qwen 2.5, DeepSeek R1).
- Host hardware specifications: Available RAM, GPU VRAM (NVIDIA CUDA, Apple Metal, or CPU).
- Local serving framework (Ollama, vLLM, or llama.cpp server).

## 5. Expected Outputs & Artifacts
- Service orchestration configuration (Docker Compose / Systemd / CLI runner).
- Client integration adapter adhering to OpenAI-compatible `/v1/chat/completions` API.
- Performance and latency benchmark report (Tokens per Second, Time to First Token - TTFT).

## 6. Step-by-Step Operating Procedure
1. **Hardware & VRAM Budget Calculation**:
   - Calculate model memory footprint: `Memory (GB) ≈ Parameters (B) * Bits_per_weight / 8 * 1.2` (including KV cache).
   - Select appropriate quantization: Q4_K_M for balanced quality/speed, Q8_0 or 16-bit for uncompromised precision.
2. **Local Engine Deployment**:
   - Launch server via Ollama (`ollama run llama3.1`) or vLLM (`vllm serve meta-llama/Llama-3.1-8B-Instruct --gpu-memory-utilization 0.9`).
3. **OpenAI-Compatible Client Adapter**:
   - Point application client to `http://localhost:11434/v1` (Ollama) or `http://localhost:8000/v1` (vLLM).
4. **Streaming & Structured Output Enforcement**:
   - Enable Server-Sent Events (SSE) streaming for real-time response rendering.
   - Enforce JSON schema constraints using grammar-based sampling (`response_format={"type": "json_object"}`).
5. **Benchmarking & Health Monitoring**:
   - Measure TTFT and tokens per second using concurrent request benchmarks.

## 7. Repository Inspection & Planning Requirements
- Non-destructive hardware and engine detection:
  ```bash
  # Check GPU
  nvidia-smi 2>/dev/null || echo "No NVIDIA GPU found; checking CPU/Apple Metal"
  # Check Ollama service
  curl -s http://localhost:11434/api/tags || echo "Ollama not running"
  ```
- Preservation rule: Never download massive multi-gigabyte models without user confirmation and disk space check.

## 8. Tool & Dependency Requirements
- Ollama CLI / vLLM / llama.cpp binary, `curl`, Python `openai` SDK or Node.js `openai` client.

## 9. Implementation Guidelines & Best Practices
- Always set keep-alive parameters properly to prevent constant model reloading overhead:
  ```python
  from openai import OpenAI

  # Connect to local Ollama instance via OpenAI SDK
  client = OpenAI(
      base_url="http://localhost:11434/v1",
      api_key="ollama" # required dummy string
  )

  response = client.chat.completions.create(
      model="llama3.1:8b",
      messages=[{"role": "user", "content": "Explain vector indexing concisely."}],
      temperature=0.2,
      stream=True
  )

  for chunk in response:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
  ```

## 10. Error Handling & Recovery Procedures
- Out of Memory (CUDA OOM): Reduce context length (`num_ctx 2048`), lower quantization level, or offload fewer layers to GPU (`--n-gpu-layers`).
- Slow token generation: Verify if GPU acceleration is active vs CPU fallback.

## 11. Security & Privacy Constraints
- Air-gapped privacy guarantee: Bind local server to `127.0.0.1` rather than `0.0.0.0` unless protected by reverse proxy authentication.

## 12. Verification & Testing Requirements
- Test inference endpoint health:
  ```bash
  curl http://localhost:11434/v1/models
  ```
- Run automated latency benchmark:
  ```bash
  python -c "
  import time
  from openai import OpenAI
  c = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
  t0 = time.time()
  res = c.chat.completions.create(model='llama3.1:8b', messages=[{'role':'user','content':'Ping'}])
  print(f'Response: {res.choices[0].message.content} in {time.time()-t0:.2f}s')
  "
  ```

## 13. Completion Criteria
- Model served locally with OpenAI-compatible API endpoint active.
- Streaming client functions reliably with zero network egress to third parties.
- Inference latency and throughput documented.

## 14. Relevant Official References
- Ollama Documentation (github.com/ollama/ollama).
- vLLM Architecture & PagedAttention (vllm.ai).
- llama.cpp GitHub Repository (github.com/ggerganov/llama.cpp).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Ollama 0.4+, vLLM 0.6+, and GGUF v3 format.
