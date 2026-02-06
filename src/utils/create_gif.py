import cv2
from PIL import Image
import os

def create_gif(video_path, output_path, max_frames=100, resize_width=480):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    
    # Skip every 2nd frame to reduce size and increase speed
    skip_rate = 2
    
    print(f"Reading video from {video_path}...")
    while True:
        ret, frame = cap.read()
        if not ret or count >= max_frames * skip_rate:
            break
            
        if count % skip_rate == 0:
            # Resize
            h, w = frame.shape[:2]
            aspect = h / w
            new_h = int(resize_width * aspect)
            frame = cv2.resize(frame, (resize_width, new_h))
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame))
            
        count += 1
        
    cap.release()
    
    if frames:
        print(f"Saving GIF to {output_path} ({len(frames)} frames)...")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=80,  # 1000ms / 12.5 fps
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
