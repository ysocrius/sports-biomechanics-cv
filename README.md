# Sports Biomechanics Analysis (Cricket & Tennis) 🏏🎾

An AI-powered computer vision pipeline to analyze sports techniques from side-on videos using YOLOv8-pose.

<p align="center">
  <img src="demo/preview.gif" width="45%" alt="Cricket Analysis" />
  <img src="demo/preview_tennis.gif" width="45%" alt="Tennis Analysis" />
</p>

## 🚀 Key Features
- **Multi-Sport Support**: Cricket (Batting/Bowling) and Tennis (Serve).
- **Interpretability**: Translates raw angles into labels (e.g., "Good Balance", "Deep Loading").
- **Performance**: Real-time processing (25+ FPS) with lightweight models.
- **Export**: Visual overlay + detailed CSV metrics.

## 🛠️ Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
**Cricket (Default):**
```bash
python -m src.main --video input/cricket.mp4 --output output/cricket_result.mp4
```

**Tennis:**
```bash
python -m src.main --video input/tennis.mp4 --output output/tennis_result.mp4 --sport tennis
```

## 🏗 Architecture
- **Pose Engine**: `ultralytics` YOLOv8n-pose
- **Metrics**: Vector geometry for joint angles (Knee/Elbow) + Center of Mass
- **Visualization**: OpenCV overlay
- **Structure**: Modular (`PoseDetector`, `MetricsEngine`, `Visualizer`)

## 📂 Documentation
- **Architecture & Thinking**: [PROJECT_REPORT.md](docs/global/PROJECT_REPORT.md)
- **Future Roadmap**: [FUTURE_ENHANCEMENTS.md](docs/global/FUTURE_ENHANCEMENTS.md)
- **Quick Guide**: [QUICKSTART.md](QUICKSTART.md)

## 📦 Project Structure
```text
src/            # Source code
docs/           # Documentation (Global & Private)
submission/     # Final deliverable package
```
