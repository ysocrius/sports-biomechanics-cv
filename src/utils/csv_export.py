"""Export metrics and keypoints to CSV."""
import pandas as pd
from typing import List, Dict

def export_metrics_to_csv(metrics_list: List[Dict], output_path: str):
    """Export frame-by-frame metrics to CSV."""
    df = pd.DataFrame(metrics_list)
    df.to_csv(output_path, index=False)
    print(f"Exported {len(df)} frames to {output_path}")

def export_keypoints_to_csv(all_landmarks: List[List[Dict]], output_path: str):
    """Export raw keypoints to CSV (frame, keypoint_id, x, y, visibility)."""
    rows = []
    for frame_idx, landmarks in enumerate(all_landmarks):
        for kp in landmarks:
            rows.append({
                'frame': frame_idx,
                'keypoint_id': kp['id'],
                'x': kp['x'],
                'y': kp['y'],
                'px': kp['px'],
                'py': kp['py'],
                'visibility': kp['visibility']
            })
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Exported {len(rows)} keypoints to {output_path}")
