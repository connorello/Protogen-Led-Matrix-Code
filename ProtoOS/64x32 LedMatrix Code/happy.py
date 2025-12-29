from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageSequence
import time
import signal
import sys

# === Matrix Configuration ===
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2     # Two 64x32 panels = 128x32
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=options)

# === Graceful Exit ===
running = True
def signal_handler(sig, frame):
    global running
    running = False
signal.signal(signal.SIGINT, signal_handler)

# === Load GIFs ===
try:
    gif_left = Image.open("happyL.gif")   # 64x32
    gif_right = Image.open("happyR.gif") # 64x32
except FileNotFoundError as e:
    print(f"Missing file: {e}")
    sys.exit(1)

# === Helper: Get max frame count ===
frames_left = [frame.copy() for frame in ImageSequence.Iterator(gif_left)]
frames_right = [frame.copy() for frame in ImageSequence.Iterator(gif_right)]
frame_count = max(len(frames_left), len(frames_right))

# === Main Loop ===
frame_index = 0
while running:
    frame_L = frames_left[frame_index % len(frames_left)].resize((64, 32)).convert("RGB")
    frame_R = frames_right[frame_index % len(frames_right)].resize((64, 32)).convert("RGB")

    # Combine into one 128x32 frame
    combined = Image.new("RGB", (128, 32))
    combined.paste(frame_L, (0, 0))    # Left matrix
    combined.paste(frame_R, (64, 0))   # Right matrix

    # Display the frame
    matrix.SetImage(combined)

    # Use left GIF's frame duration or default
    duration = frames_left[frame_index % len(frames_left)].info.get("duration", 100)
    time.sleep(duration / 1000.0)

    frame_index += 1
