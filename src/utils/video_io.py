import cv2
import logging
import numpy as np
from typing import Iterator, Tuple, Optional

logger = logging.getLogger(__name__)

class VideoStream:
    """
    Handle video input and output streams.
    """
    def __init__(self, input_path: str, output_path: Optional[str] = None):
        self.input_path = input_path
        self.output_path = output_path
        self.cap = cv2.VideoCapture(input_path)
        self.writer = None
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video file: {input_path}")
            
        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Video opened: {self.width}x{self.height} @ {self.fps}fps")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def frames(self) -> Iterator[Tuple[bool, np.ndarray]]:
        """Yield frames from the video."""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            yield ret, frame

    def setup_writer(self, output_path: str = None):
        """Initialize the video writer."""
        path = output_path or self.output_path
        if not path:
            logger.warning("No output path specified for writer")
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            path, fourcc, self.fps, (self.width, self.height)
        )
        logger.info(f"Video writer initialized: {path}")

    def write_frame(self, frame: np.ndarray):
        """Write a frame to the output video."""
        if self.writer:
            self.writer.write(frame)

    def release(self):
        """Release resources."""
        if self.cap:
            self.cap.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
