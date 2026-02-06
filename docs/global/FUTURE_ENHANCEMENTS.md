# Future Enhancements Roadmap

## 1. Technical Optimizations

### Temporal Smoothing (Kalman Filter)
- **Problem**: Keypoint jitter (high frequency noise) affects angle calculation.
- **Solution**: Implement a Kalman Filter or One-Euro Filter to smooth trajectories over time.
- **Impact**: More stable metric graphs and fewer outliers.

### Model Upgrades
- **Current**: YOLOv8n-pose (Nano) - Optimized for speed.
- **Proposed**: YOLOv8m-pose or RTMPose-l.
- **Trade-off**: Higher accuracy vs. lower FPS.

### 3D Pose Reconstruction
- **Limitation**: 2D angles (projected) don't represent true biomechanics.
- **Upgrade**: Use `VideoPose3D` or `MediaPipe 3D` (when API stabilizes) to lift 2D keypoints to 3D space.

---

## 2. Product Features

### Multi-Person Analysis
- **Current**: Processes first detected person.
- **Future**: ID tracking (BoTSORT) to handle multiple players (e.g., batsman + runner).

### Automated Phase Detection
- **Feature**: Automatically segment video into "Run-up", "Delivery", and "Follow-through".
- **Method**: Heuristic-based (velocity thresholds) or LSTM-based action classifier.

### Web Dashboard
- **Current**: CLI + CSV output.
- **Future**: Streamlit/React app for interactive graph exploration and side-by-side video comparison.

---

## 3. Data Strategy

### Cricket-Specific Fine-tuning
- **Dataset**: Curate 500+ clips of bowling actions.
- **Labeling**: Manually correct occlusions (e.g., ball hiding hand).
- **Goal**: Reduce "limb swapping" errors during complex movements.
