---
name: computer-vision-engineer
description: Computer vision engineering with OpenCV, PyTorch Vision, YOLOv8/v11, ONNX Runtime inference, real-time object detection, segmentation, and edge device optimization.
---

# Computer Vision & Real-Time Object Detection

## 1. Intended Role & Domain
- **Primary Domain**: Artificial Intelligence & Computer Vision
- **Target Roles**: Computer Vision Engineer, Edge AI Engineer, Robotics Software Developer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "computer vision", "opencv", "yolo object detection", "image segmentation", "onnx vision inference", "real-time video processing".
- **Contextual Inferences**: Repositories containing `cv2`, `torchvision`, `ultralytics`, image/video processing pipelines.
- **Chained Predecessors**: `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Working purely with natural language text or audio waveforms without image or video inputs.
  - Basic CSS styling for web images.

## 4. Required Inputs & Context
- Image or video stream input source.
- Model architecture (YOLOv8/v11, MobileNet, Segment Anything Model - SAM, ResNet).
- Inference target: GPU (CUDA/TensorRT), CPU (ONNX Runtime), or Edge device (Raspberry Pi/Jetson).

## 5. Expected Outputs & Artifacts
- Preprocessing and augmentation pipeline (normalization, color space conversion, letterboxing).
- Batched inference runner with Non-Maximum Suppression (NMS).
- Exported ONNX / TensorRT engine model artifact for production deployment.
- Annotated output generator with bounding boxes, confidence scores, and class labels.

## 6. Step-by-Step Operating Procedure
1. **Input Preprocessing & Letterboxing**:
   - Maintain aspect ratio by letterboxing images with zero/gray padding to model input dimensions (e.g. 640x640).
   - Convert BGR (OpenCV default) to RGB and normalize pixel intensities to `[0.0, 1.0]`.
2. **Model Loading & Hardware Optimization**:
   - Load pre-trained or fine-tuned weights using PyTorch or ONNX Runtime with hardware execution providers (`CUDAExecutionProvider`, `CPUExecutionProvider`).
3. **Forward Pass & Post-Processing**:
   - Run inference and extract raw output tensors.
   - Apply Non-Maximum Suppression (NMS) with configurable IoU threshold (e.g. 0.45) and confidence threshold (e.g. 0.5) to eliminate duplicate detections.
4. **Coordinate Scaling & Annotation**:
   - Rescale bounding boxes back to the original source resolution coordinates.
5. **Validation & FPS Benchmarking**:
   - Benchmark inference speed and ensure FPS target (e.g. >= 30 FPS for real-time video).

## 7. Repository Inspection & Planning Requirements
- Check vision packages:
  ```bash
  python -c "import cv2, onnxruntime; print('OpenCV:', cv2.__version__, 'ONNX:', onnxruntime.__version__)" 2>/dev/null || echo "Vision libs not installed"
  ```
- Preservation rule: Avoid memory leaks in video loops; always release video capture objects (`cap.release()`).

## 8. Tool & Dependency Requirements
- Python 3.10+, OpenCV (`opencv-python-headless`), `onnxruntime`, `numpy`, `torchvision` or `ultralytics`.

## 9. Implementation Guidelines & Best Practices
- Avoid dynamic resizing allocations in the inner video loop; allocate buffer arrays once.
- Always use `opencv-python-headless` in server/container environments to avoid missing X11/GUI display library errors.

```python
import cv2
import numpy as np
import onnxruntime as ort

class VisionDetector:
    def __init__(self, onnx_model_path: str):
        self.session = ort.InferenceSession(onnx_model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        # Resize, BGR to RGB, transpose HWC -> CHW, normalize
        resized = cv2.resize(frame, (640, 640))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = rgb.astype(np.float32) / 255.0
        return np.expand_dims(np.transpose(tensor, (2, 0, 1)), axis=0)
```

## 10. Error Handling & Recovery Procedures
- Missing GPU execution provider: Wrap ONNX Runtime provider initialization in a try-catch and fall back gracefully to `CPUExecutionProvider`.
- Corrupt image input: Validate `img is not None` before preprocessing to avoid OpenCV C++ assertions.

## 11. Security & Privacy Constraints
- Protect biometric data: Ensure facial recognition or license plate data complies with local privacy regulations (GDPR, CCPA); blur sensitive areas when required.

## 12. Verification & Testing Requirements
- Test inference on sample validation image:
  ```bash
  python -c "
  import numpy as np
  from detector import VisionDetector
  det = VisionDetector('model.onnx')
  dummy = np.zeros((480, 640, 3), dtype=np.uint8)
  out = det.preprocess(dummy)
  assert out.shape == (1, 3, 640, 640)
  print('Preprocess test PASSED')
  "
  ```

## 13. Completion Criteria
- Model runs inference successfully on static images and video streams.
- NMS filtering produces accurate single bounding boxes per entity.
- Latency meets defined threshold.

## 14. Relevant Official References
- OpenCV Documentation (docs.opencv.org).
- ONNX Runtime Inference API (onnxruntime.ai).
- Ultralytics YOLOv8/v11 Architecture.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with ONNX IR v9+ and OpenCV 4.10+.
