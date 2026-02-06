# Project Report: Sports Biomechanics Analysis

## 1. Architecture & Approach
**Pipeline**: Video → Pose Detection (YOLOv8) → Metrics Calculation → Overlay Visualization → Output

**Tech Stack**:
- **Pose Estimation**: YOLOv8n-pose (ultralytics)
- **Video I/O**: OpenCV
- **Metrics**: NumPy vector geometry
- **Visualization**: Real-time overlay on video frames

## 2. Model Selection
- **Model**: YOLOv8n-pose
- **Rationale**: 
  - Stable API (vs MediaPipe 0.10.x breaking changes)
  - Better for sports (trained on COCO keypoints)
  - Real-time performance (25 FPS on 720p)
  - Built-in visualization

## 3. Key Metrics (Implemented)
1. **Knee Angle**: Hip-Knee-Ankle flexion (172.5° avg = "Straight stance")
2. **Elbow Angle**: Shoulder-Elbow-Wrist flexion (bowling arm mechanics)
3. **Center of Mass**: Torso midpoint (hip+shoulder average) for stability tracking

**Interpretations**:
- **Cricket**: >160° Knee = "Straight"
- **Tennis**: <120° Knee = "Good Serve Loading" (Dynamic adaptation)

## 4. Challenges & Solutions

### MediaPipe API Breaking Change
**Challenge**: `mediapipe 0.10.32` removed `mp.solutions` API  
**Solution**: Switched to YOLOv8-pose (6MB model, stable API)  
**Impact**: +2 hours debugging, but better long-term stability

### Module Import Errors
**Challenge**: `ModuleNotFoundError: No module named 'src'`  
**Solution**: Run as module (`python -m src.main`) to preserve namespace  
**Lesson**: Always use `-m` flag for package scripts

## 5. Model Improvement Thinking

### Q1: What problems did you observe?
- **Keypoint Jitter**: Slight frame-to-frame instability in wrist/ankle positions (±5px)
- **Occlusion Handling**: When player turns sideways, far-side limbs have low confidence (<0.3)
- **Motion Blur**: Fast bowling actions cause temporary keypoint loss

### Q2: How would you improve accuracy with more time/data?
**Architecture**:
- Switch to **YOLOv8m-pose** (larger model, +10% accuracy, 15 FPS)
- Add **temporal smoothing** (Kalman filter on keypoint trajectories)
- Fine-tune on cricket-specific dataset (100+ videos)

**Data Augmentation**:
- Synthetic occlusion masks during training
- Multi-angle camera views (front + side)

### Q3: What data would you collect?
- **Cricket-specific dataset**: 500+ videos (batting, bowling, fielding)
- **Annotations**: Manual keypoint corrections for occluded frames
- **Metadata**: Player height, camera distance (for normalization)
- **Multi-view sync**: Stereo cameras for 3D pose reconstruction

### Q4: How would you split Train/Validation/Test?
- **Train**: 70% (350 videos) - Diverse players, lighting, angles
- **Val**: 15% (75 videos) - Held-out players for generalization check
- **Test**: 15% (75 videos) - Completely unseen match footage

**Stratification**: Balance by action type (batting/bowling/fielding)

### Q5: How would you evaluate improvement?
**Quantitative Metrics**:
- **PCK@0.1** (Percentage of Correct Keypoints within 10% of torso diameter)
- **OKS** (Object Keypoint Similarity - COCO standard)
- **Temporal Consistency**: Frame-to-frame jitter reduction (MPJPE)

**Qualitative**:
- Expert review (cricket coaches validate biomechanics)
- A/B test: Current vs improved model on same video


