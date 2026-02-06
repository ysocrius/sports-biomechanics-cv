import cv2
import argparse
import logging
from src.pose_engine.detector import PoseDetector
from src.metrics.analyzer import MetricsEngine
from src.utils.video_io import VideoStream
from src.utils.csv_export import export_metrics_to_csv, export_keypoints_to_csv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Sports Biomechanics Analysis")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--output", type=str, default="output/result.mp4", help="Path to output video")
    parser.add_argument("--sport", type=str, default="cricket", choices=["cricket", "tennis"], help="Sport type for metrics")
    args = parser.parse_args()
    
    detector = PoseDetector()
    metrics_engine = MetricsEngine(sport_type=args.sport)
    all_landmarks = []  # Store all frame landmarks
    
    try:
        with VideoStream(args.video, args.output) as stream:
            stream.setup_writer()
            
            frame_count = 0
            for ret, frame in stream.frames():
                if not ret:
                    break
                
                # Pose detection
                results = detector.process_frame(frame)
                
                # Extract landmarks
                landmarks = detector.extract_landmarks(results, (frame.shape[0], frame.shape[1]))
                all_landmarks.append(landmarks)
                
                # Calculate metrics
                metrics = metrics_engine.calculate_frame_metrics(landmarks)
                
                # Visualize skeleton
                annotated_frame = detector.draw_landmarks(frame, results)
                
                # Overlay metrics text
                if metrics:
                    y_offset = 30
                    cv2.putText(annotated_frame, f"Knee Angle: {metrics.get('knee_angle_right', 0):.1f}° ({metrics.get('knee_status', '')})", 
                               (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Elbow Angle: {metrics.get('elbow_angle_right', 0):.1f}°", 
                               (10, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Write frame
                stream.write_frame(annotated_frame)
                
                frame_count += 1
                if frame_count % 30 == 0:
                    print(f"Processed {frame_count} frames...", end='\r')
            
            # Summary stats
            stats = metrics_engine.get_summary_stats()
            logger.info(f"Summary: Avg Knee Angle = {stats.get('avg_knee_angle', 0):.1f}°")
            logger.info("Processing complete!")
            
            # Export CSVs
            export_metrics_to_csv(metrics_engine.frame_metrics, "output/metrics.csv")
            export_keypoints_to_csv(all_landmarks, "output/keypoints.csv")
            
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
