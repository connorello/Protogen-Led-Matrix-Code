from flask import Flask, render_template, request, jsonify
import subprocess
import os
import signal

# Initialize the Flask app
app = Flask(__name__)

# Path to your GIFs folder
GIFS_FOLDER = "/home/pi/ProtoOS/64x32 LedMatrix Code/gifs"
running_process = None  # Variable to track the current running process

def stop_running_process():
    global running_process
    if running_process:
        running_process.terminate()
        running_process = None

@app.route('/')
def index():
    # List all Python files in the gifs directory
    gif_files = [f for f in os.listdir(GIFS_FOLDER) if f.endswith('.py')]
    return render_template('index.html', gif_files=gif_files)

@app.route('/run_gif', methods=['POST'])
def run_gif():
    global running_process
    gif_file = request.form['gif_file']

    # Stop the currently running process if any
    stop_running_process()

    # Run the new Python file
    gif_path = os.path.join(GIFS_FOLDER, gif_file)
    running_process = subprocess.Popen(['python3', gif_path])

    return jsonify({"status": "success", "message": f"Running {gif_file}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
