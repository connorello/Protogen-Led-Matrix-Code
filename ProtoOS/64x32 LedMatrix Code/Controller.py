import pygame
import subprocess
import time
import os
import signal
import threading
import RPi.GPIO as GPIO

# --- Setup GPIO for touch sensor ---
TOUCH_PIN = 25   # Pin 22 = GPIO25
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)

# --- Setup pygame for controller ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller connected: {joystick.get_name()}")

# --- Button-to-script map ---
button_script_map = {
    0: 'happy.py',  # Usually X / A
    1: 'blank.py',  # Circle / B
    2: 'owo.py',
    3: 'blank.py',
}

# --- D-pad (hat) to script map ---
hat_script_map = {
    (0, 1): 'blank.py',
    (0, -1): 'blank.py',
    (-1, 0): 'blank.py',
    (1, 0): 'blank.py',
}

# --- Touch sensor script ---
touch_script = 'blank.py'
touch_running = False

current_process = None

def run_script(script):
    """Kill previous script and start a new one."""
    global current_process
    if current_process and current_process.poll() is None:
        print("Stopping previous script...")
        os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
    print(f"Starting {script}...")
    current_process = subprocess.Popen(
        ['python3', script],
        preexec_fn=os.setsid
    )

def toggle_touch_script():
    """Toggle the touch script on/off."""
    global current_process, touch_running
    if touch_running:
        if current_process and current_process.poll() is None:
            print("Stopping touch.py")
            os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
        touch_running = False
    else:
        print("Starting touch.py")
        current_process = subprocess.Popen(
            ['python3', touch_script],
            preexec_fn=os.setsid
        )
        touch_running = True

# --- Thread: Watch for touch sensor ---
def watch_touch():
    prev_state = 0
    while True:
        state = GPIO.input(TOUCH_PIN)
        if state == 1 and prev_state == 0:  # Detect rising edge
            toggle_touch_script()
            time.sleep(0.2)  # debounce
        prev_state = state
        time.sleep(0.05)

threading.Thread(target=watch_touch, daemon=True).start()

# --- Main loop: Controller buttons + D-pad ---
try:
    while True:
        pygame.event.pump()

        # Controller buttons
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                if i in button_script_map:
                    run_script(button_script_map[i])
                    time.sleep(0.5)  # debounce

        # D-pad (hat)
        if joystick.get_numhats() > 0:
            hat = joystick.get_hat(0)
            if hat in hat_script_map and hat != (0, 0):
                run_script(hat_script_map[hat])
                time.sleep(0.5)

        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")