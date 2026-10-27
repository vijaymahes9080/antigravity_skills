---
name: ai-inference-infrastructure
description: High-throughput low-latency GPU inference serving, continuous batching, PagedAttention, KV-cache optimization, TensorRT-LLM, vLLM cluster deployment, quantization (FP8/AWQ), and inference latency SLOs.
---

# AI Inference Infrastructure & High-Performance Serving

## 1. Intended Role & Domain
- **Primary Domain**: AI Infrastructure & Safety
- **Target Roles**: AI Infrastructure Engineer, ML Systems Architect, High-Performance Inference Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "gpu inference", "vllm deployment", "tensorrt-llm", "kv cache optimization", "continuous batching", "pagedattention", "inference latency slo", "fp8 quantization", "awq inference", "model serving cluster".
- **Contextual Inferences**: Deploying high-throughput LLM backends to Kubernetes/bare-metal, optimizing time-to-first-token (TTFT) and inter-token latency (ITL).
- **Chained Predecessors**: `local-llm-integration`, `docker-containerization`, `site-reliability-sre`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Running lightweight local CPU inference for small one-off dev tasks -> use `/local-llm-integration`.
  - Designing web UI chat widgets -> use `/react-nextjs-pro`.

## 4. Required Inputs & Context
- Target model architecture (Llama 3.x, Mistral, DeepSeek, Qwen).
- Hardware topography (NVIDIA H100, A100, L40S, AMD MI300X, or Apple Silicon).
- SLA / SLO targets: TTFT < 200ms, ITL < 20ms, Target Concurrency (req/sec).
- Serving engine preference (vLLM, TensorRT-LLM, TGI).

## 5. Expected Outputs & Artifacts
- Production Docker compose or Kubernetes manifests (`vllm-deployment.yaml`) with GPU resource allocations.
- Optimized engine configuration (tensor parallelism, pipeline parallelism, max model length, GPU memory utilization).
- Benchmarking harness (`benchmark_throughput.py`) reporting TTFT, ITL, and tokens/sec/GPU.
- Prometheus exporter metrics configuration for inference health monitoring.

## 6. Step-by-Step Operating Procedure
1. **Model & Precision Selection**:
   - Determine target quantization format (FP16, BF16, FP8 W8A8, or INT4-AWQ) balancing perplexity against VRAM budget.
2. **GPU Memory & KV-Cache Sizing**:
   - Calculate static model weight memory + KV-cache allocation:
     `KV_Cache_Size = 2 * n_layers * n_heads * head_dim * precision_bytes * max_seq_len * batch_size`
   - Set `gpu_memory_utilization: 0.90` with PagedAttention to eliminate memory fragmentation.
3. **Engine Configuration & Parallelism**:
   - Set Tensor Parallelism (`tp=N`) matching single-node GPU count; Pipeline Parallelism (`pp=N`) across multi-node InfiniBand networks.
4. **Continuous Batching & Chunked Prefill**:
   - Enable chunked prefill to prevent large prompt context from starving token generation in concurrent requests.
5. **Observability & Health SLOs**:
   - Expose metrics: `vllm:num_requests_waiting`, `vllm:gpu_cache_usage_factor`, `vllm:time_to_first_token_seconds`.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of existing inference configurations:
  ```bash
  find . -name "*vllm*" -o -name "*tensorrt*" -o -name "*inference*.py" 2>/dev/null
  ```
- Hardware validation: Confirm compute capability (`sm_80`, `sm_89`, `sm_90`) before choosing FP8/BF16 kernels.

## 8. Tool & Dependency Requirements
- NVIDIA Container Toolkit, CUDA 12.4+, vLLM >= 0.6.0, TensorRT-LLM, PyTorch 2.4+.

## 9. Implementation Guidelines & Best Practices
- Production Kubernetes deployment manifest for vLLM with high-throughput continuous batching:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama3-serving
  labels:
    app: vllm-llama3
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm-llama3
  template:
    metadata:
      labels:
        app: vllm-llama3
    spec:
      containers:
      - name: vllm-server
        image: vllm/vllm-openai:v0.6.3
        args:
        - "--model"
        - "meta-llama/Meta-Llama-3.1-70B-Instruct"
        - "--tensor-parallel-size"
        - "4"
        - "--max-model-len"
        - "8192"
        - "--gpu-memory-utilization"
        - "0.92"
        - "--enable-chunked-prefill"
        - "--kv-cache-dtype"
        - "auto"
        - "--port"
        - "8000"
        resources:
          limits:
            nvidia.com/gpu: "4"
            memory: "128Gi"
            cpu: "16"
          requests:
            nvidia.com/gpu: "4"
            memory: "64Gi"
            cpu: "8"
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 10
```

## 10. Error Handling & Recovery Procedures
- CUDA Out of Memory (OOM) during prefill: Lower `max_num_batched_tokens` and reduce `gpu_memory_utilization` to `0.88`.
- KV Cache exhaustion: Verify request queueing alerts; scale out replicas horizontally via Horizontal Pod Autoscaler (HPA).

## 11. Security & Privacy Constraints
- Never expose raw inference endpoints without mTLS or API token authentication.
- Secure model weights stored in local PVC cache with restricted read-only permissions.

## 12. Verification & Testing Requirements
- Benchmark TTFT < 250ms at 95th percentile under concurrent load.
- Zero unexpected engine crashes during long-context (8k+ tokens) requests.
- GPU utilization remains > 80% under standard request volume.

## 13. Completion Criteria
- Serving engine successfully initialized and passing `/health` checks.
- OpenAI-compatible `/v1/chat/completions` API endpoint verified.
- Prometheus telemetry dashboard operational.

## 14. Relevant Official References
- vLLM Architecture & PagedAttention Whitepaper (Kwon et al.).
- NVIDIA TensorRT-LLM Documentation.
- FasterTransformer / FlashAttention 3 Kernel Specifications.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with CUDA 12.x, Triton, and Ampere/Hopper/Blackwell GPU architectures.
