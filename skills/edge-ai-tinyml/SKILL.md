---
name: edge-ai-tinyml
description: Deploy machine learning models on resource-constrained microcontrollers and edge devices using TinyML, TensorFlow Lite Micro, INT8 post-training quantization, and CMSIS-NN hardware acceleration.
---

# Edge AI & TinyML Model Deployment

## 1. Intended Role & Domain
- **Primary Domain**: Embedded Systems & Artificial Intelligence
- **Target Roles**: Edge AI Engineer, Embedded Systems Engineer, IoT Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "edge ai", "tinyml", "tensorflow lite micro", "tflite micro", "int8 quantization", "cmsis-nn", "microcontroller ml", "edge impulse".
- **Contextual Inferences**: Running keyword spotting, anomaly detection, or sensor classification on microcontrollers with < 512KB RAM.
- **Chained Predecessors**: `embedded-firmware-c`, `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Running multi-billion parameter LLMs on cloud clusters.
  - Standard desktop deep learning training without embedded deployment constraints.

## 4. Required Inputs & Context
- Pre-trained neural network (Keras, PyTorch, or ONNX).
- Representative calibration dataset for quantization.
- Target hardware specs: Flash size (ROM), SRAM buffer limits (e.g. 64KB - 256KB), CPU clock speed.

## 5. Expected Outputs & Artifacts
- Quantized TFLite flatbuffer (`model_int8.tflite`).
- Generated C byte array (`model_data.h`).
- Embedded inference runner allocating static tensor arena.
- Latency and RAM benchmark report.

## 6. Step-by-Step Operating Procedure
1. **Model Pruning & Architecture Optimization**:
   - Limit operations to supported TinyML kernels (DepthwiseConv2D, FullyConnected, Pooling, Softmax).
2. **Post-Training Full Integer Quantization (INT8)**:
   - Quantize float32 weights and activations to int8 using a representative dataset generator.
   - Enforce pure integer operations: `converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]`.
3. **C Header Generation**:
   - Convert binary `.tflite` into C byte array using `xxd -i model_int8.tflite > model_data.h`.
4. **Static Tensor Arena Allocation**:
   - Allocate fixed memory buffer in embedded C++ (`uint8_t tensor_arena[ARENA_SIZE]`).
   - Profile arena size using `tflite::MicroInterpreter`.
5. **Hardware Acceleration (CMSIS-NN)**:
   - Enable ARM CMSIS-NN SIMD optimizations in compilation flags (`-DARM_MATH_DSP -DCMSIS_NN`).

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of model converter and toolchain:
  ```bash
  python -c "import tensorflow as tf; print('TF version:', tf.__version__)" 2>/dev/null || echo "TensorFlow not installed"
  ```
- Preservation rule: Never allocate tensor arenas dynamically from the heap; allocate in static BSS segment.

## 8. Tool & Dependency Requirements
- TensorFlow 2.x / TFLite Micro, Python 3.10+, GNU Arm Embedded Toolchain (`arm-none-eabi-gcc`), xxd.

## 9. Implementation Guidelines & Best Practices
- Verify model accuracy retention after quantization: degradation between Float32 and INT8 should be < 2%.
- Keep tensor arena small by reusing memory across non-overlapping layer activations.

```cpp
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "model_data.h"

constexpr int kTensorArenaSize = 40 * 1024; // 40KB
alignas(16) uint8_t tensor_arena[kTensorArenaSize];

void RunInference() {
    const tflite::Model* model = tflite::GetModel(g_model_data);
    tflite::AllOpsResolver resolver;
    tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, kTensorArenaSize);
    
    TfLiteStatus status = interpreter.AllocateTensors();
    if (status != kTfLiteOk) return;

    TfLiteTensor* input = interpreter.input(0);
    // Populate input->data.int8 with sensor samples...
    
    interpreter.Invoke();
    
    TfLiteTensor* output = interpreter.output(0);
    // Read output->data.int8 classification scores...
}
```

## 10. Error Handling & Recovery Procedures
- `AllocateTensors() failed`: Tensor arena is too small; increase `kTensorArenaSize` in 4KB increments until allocation succeeds.
- Unsupported operator: Replace exotic activation or layer with standard supported equivalents (e.g. replace LeakyReLU with standard ReLU).

## 11. Security & Privacy Constraints
- Edge privacy advantage: Sensor data is processed entirely on-device; never transmit raw microphone or image feeds over unencrypted networks.

## 12. Verification & Testing Requirements
- Verify model file size:
  ```bash
  ls -lh model_int8.tflite
  ```
- Run unit test comparing Python float32 inference with embedded INT8 output on test samples.

## 13. Completion Criteria
- Model successfully converted to INT8 with C array generated.
- Model fits within target microcontroller Flash (< 200KB) and SRAM (< 64KB).
- Tensor allocation and inference pass cleanly.

## 14. Relevant Official References
- TensorFlow Lite for Microcontrollers (tensorflow.org/lite/microcontrollers).
- ARM CMSIS-NN Neural Network Library for Cortex-M.
- Pete Warden & Daniel Situnayake: "TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers".

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with TFLite Micro 2.16+ and CMSIS 6.0+.
