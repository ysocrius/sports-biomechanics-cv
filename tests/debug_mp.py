import mediapipe as mp
import os
import sys

print(f"Python: {sys.version}")
print(f"MediaPipe Version: {mp.__version__}")
print(f"MediaPipe Location: {mp.__file__}")

print("\n--- dir(mp) ---")
print(dir(mp))

try:
    from mediapipe import solutions
    print("\n'from mediapipe import solutions' SUCCESS")
    print(dir(solutions))
except Exception as e:
    print(f"\n'from mediapipe import solutions' FAILED: {e}")

try:
    import mediapipe.python.solutions as solutions_direct
    print("\n'import mediapipe.python.solutions' SUCCESS")
except Exception as e:
    print(f"\n'import mediapipe.python.solutions' FAILED: {e}")

