import cv2
from PIL import Image
import os

def center_crop_resize(frame, target_w=400, target_h=300):
    """Resizes and center crops visual frame to target dimensions."""
    h, w = frame.shape[:2]
    
    # Calculate scale needed to cover target dimensions
    scale_w = target_w / w
    scale_h = target_h / h
    scale = max(scale_w, scale_h)
    
    # Resize keeping aspect ratio
    new_w = int(w * scale)
    new_h = int(h * scale)
    frame = cv2.resize(frame, (new_w, new_h))
    
    # Center crop
    start_x = (new_w - target_w) // 2
    start_y = (new_h - target_h) // 2
    return frame[start_y:start_y+target_h, start_x:start_x+target_w]

def create_gif(video_path, output_path, max_frames=100):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    skip_rate = 2
    
    print(f"Reading video from {video_path}...")
    while True:
        ret, frame = cap.read()
        if not ret or count >= max_frames * skip_rate:
            break
            
        if count % skip_rate == 0:
            # Smart Resize & Crop
            frame = center_crop_resize(frame, 400, 300)
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame))
            
        count += 1
        
    cap.release()
    
    if frames:
        print(f"Saving Standardized GIF to {output_path} (400x300)...")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=80,
            loop=0,
            optimize=True
        )
        print("Done!")
    else:
        print("No frames extracted.")

if __name__ == "__main__":
    # Convert Cricket
    if os.path.exists("demo/final_output.mp4"):
        create_gif("demo/final_output.mp4", "demo/preview.gif")
    
    # Convert Tennis
    if os.path.exists("demo/tennis_output.mp4"):
        create_gif("demo/tennis_output.mp4", "demo/preview_tennis.gif")
