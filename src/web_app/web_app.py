import os
import sys
import subprocess
import threading
import time
import json
import uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import webbrowser
import requests

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- CONFIG ---
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../../assets/images/image.png')
GLB_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../../assets/models/exported_label.glb')
BLEND_FILE = os.path.join(os.path.dirname(__file__), '../../assets/blend_files/Golf.blend')
BLENDER_DIR = r"C:\Program Files\Blender Foundation\Blender 4.4"
BLENDER_EXE = os.path.join(BLENDER_DIR, "blender.exe")
WEB_APP_DIR = os.path.join(os.path.dirname(__file__), '../viewer/w3')

# Global variables for pipeline status
pipeline_status = {
    'is_running': False,
    'current_step': None,
    'progress': 0,
    'error': None,
    'web_viewer_url': None
}

def check_dependencies():
    """Check if all required dependencies exist."""
    issues = []
    
    # Check .env file
    if not os.path.exists(".env"):
        issues.append("Missing .env file with OpenAI API key")
    
    # Check Blender
    if not os.path.exists(BLENDER_EXE):
        issues.append(f"Blender not found at: {BLENDER_EXE}")
    
    # Check .blend file
    if not os.path.exists(BLEND_FILE):
        issues.append(f"Blender file not found: {BLEND_FILE}")
    
    # Check required scripts
    required_scripts = [os.path.join(os.path.dirname(__file__), '../../scripts/generate_image_with_dalle.py'), os.path.join(os.path.dirname(__file__), '../blender/generate_label_glb.py')]
    for script in required_scripts:
        if not os.path.exists(script):
            issues.append(f"Required script not found: {script}")
    
    # Check web app directory
    if not os.path.exists(WEB_APP_DIR):
        issues.append(f"Web app directory not found: {WEB_APP_DIR}")
    
    return issues

def run_pipeline_step(step_name, command, step_progress):
    """Run a pipeline step and emit progress updates."""
    try:
        pipeline_status['current_step'] = step_name
        pipeline_status['progress'] = step_progress
        socketio.emit('pipeline_update', pipeline_status)
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"{step_name} failed: {e.stderr}"

def run_dalle_generation(prompt):
    """Run DALL-E image generation."""
    command = [sys.executable, os.path.join(os.path.dirname(__file__), '../../scripts/generate_image_with_dalle.py'), '--prompt', prompt]
    return run_pipeline_step("Generating Image with DALL-E", command, 25)

def run_blender_export():
    """Run Blender export process."""
    command = [
        BLENDER_EXE, BLEND_FILE,
        "--background",
        "--python", os.path.join(os.path.dirname(__file__), '../blender/generate_label_glb.py'),
        "--", IMAGE_PATH, GLB_OUTPUT_PATH
    ]
    return run_pipeline_step("Updating 3D Model in Blender", command, 75)

def start_web_viewer():
    """Start the web viewer server."""
    try:
        print(f"[DEBUG] Starting web viewer from directory: {WEB_APP_DIR}")
        
        # Check if web app directory exists
        if not os.path.exists(WEB_APP_DIR):
            print(f"[ERROR] Web app directory not found: {WEB_APP_DIR}")
            return False
        
        # Check if package.json exists
        package_json = os.path.join(WEB_APP_DIR, "package.json")
        if not os.path.exists(package_json):
            print(f"[ERROR] package.json not found in: {WEB_APP_DIR}")
            return False
        
        # Find npm path
        npm_path = "npm"
        try:
            subprocess.run(["npm", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try common npm locations on Windows
            possible_npm_paths = [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
                os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps\npm.exe")
            ]
            
            for path in possible_npm_paths:
                if os.path.exists(path):
                    print(f"[INFO] Found npm at: {path}")
                    npm_path = path
                    break
            else:
                print("[ERROR] npm not found. Please install Node.js and npm.")
                return False
        
        # Install dependencies if needed
        node_modules_path = os.path.join(WEB_APP_DIR, "node_modules")
        if not os.path.exists(node_modules_path):
            print("[INFO] Installing Node.js dependencies...")
            try:
                result = subprocess.run(
                    [npm_path, "install"], 
                    cwd=WEB_APP_DIR, 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                print("[SUCCESS] Dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to install dependencies: {e.stderr}")
                return False
        

        
        # Try to start server with npm start
        print("[INFO] Starting server with npm start...")
        try:
            server_process = subprocess.Popen(
                [npm_path, "start"], 
                cwd=WEB_APP_DIR, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Check if process is still running
            if server_process.poll() is not None:
                # Process died, try direct node execution
                print("[INFO] npm start failed, trying direct node execution...")
                server_process = subprocess.Popen(
                    ["node", "server.js"], 
                    cwd=WEB_APP_DIR, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                time.sleep(3)
            
            # Check if server is running
            try:
                response = requests.get("http://localhost:3000", timeout=10)
                if response.status_code == 200:
                    print("[SUCCESS] Web viewer server is running")
                    pipeline_status['web_viewer_url'] = "http://localhost:3000"
                    return True
                else:
                    print(f"[WARN] Server responded with status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Could not connect to server: {e}")
            
            # If we get here, server didn't start properly
            print("[ERROR] Server failed to start properly")
            return False
            
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Unexpected error in start_web_viewer: {e}")
        return False

def pipeline_worker(prompt):
    """Background worker for running the pipeline."""
    global pipeline_status
    
    try:
        pipeline_status['is_running'] = True
        pipeline_status['error'] = None
        pipeline_status['progress'] = 0
        socketio.emit('pipeline_update', pipeline_status)
        
        # Step 1: Generate image
        success, error = run_dalle_generation(prompt)
        if not success:
            pipeline_status['error'] = error
            pipeline_status['is_running'] = False
            socketio.emit('pipeline_update', pipeline_status)
            return
        
        # Step 2: Update 3D model
        success, error = run_blender_export()
        if not success:
            pipeline_status['error'] = error
            pipeline_status['is_running'] = False
            socketio.emit('pipeline_update', pipeline_status)
            return
        
        # Step 3: Start web viewer
        pipeline_status['current_step'] = "Starting Web Viewer"
        pipeline_status['progress'] = 90
        socketio.emit('pipeline_update', pipeline_status)
        
        if start_web_viewer():
            pipeline_status['progress'] = 100
            pipeline_status['current_step'] = "Complete"
            socketio.emit('pipeline_update', pipeline_status)
            
            # Open browser
            webbrowser.open("http://localhost:3000")
        else:
            pipeline_status['error'] = "Failed to start web viewer"
        
        pipeline_status['is_running'] = False
        socketio.emit('pipeline_update', pipeline_status)
        
    except Exception as e:
        pipeline_status['error'] = str(e)
        pipeline_status['is_running'] = False
        socketio.emit('pipeline_update', pipeline_status)

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current pipeline status."""
    return jsonify(pipeline_status)

@app.route('/api/check-dependencies')
def check_deps():
    """Check system dependencies."""
    issues = check_dependencies()
    return jsonify({
        'issues': issues,
        'ready': len(issues) == 0
    })

@app.route('/api/generate', methods=['POST'])
def generate_label():
    """Start the label generation pipeline."""
    if pipeline_status['is_running']:
        return jsonify({'error': 'Pipeline already running'}), 400
    
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt.strip():
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Start pipeline in background thread
    thread = threading.Thread(target=pipeline_worker, args=(prompt,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Pipeline started'})

@app.route('/api/viewer')
def open_viewer():
    """Open the 3D viewer."""
    if pipeline_status['web_viewer_url']:
        webbrowser.open(pipeline_status['web_viewer_url'])
        return jsonify({'message': 'Viewer opened'})
    else:
        return jsonify({'error': 'No viewer available'}), 400

@app.route('/api/start-viewer')
def start_viewer():
    """Manually start the 3D viewer server."""
    try:
        if start_web_viewer():
            return jsonify({'message': 'Viewer started successfully', 'url': 'http://localhost:3000'})
        else:
            return jsonify({'error': 'Failed to start viewer'}), 500
    except Exception as e:
        return jsonify({'error': f'Error starting viewer: {str(e)}'}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('pipeline_update', pipeline_status)

if __name__ == '__main__':
    print("=== Golf Ball Label Generator Web App ===")
    print("Starting web application...")
    print("Access the app at: http://localhost:5000")
    
    # Check dependencies on startup
    issues = check_dependencies()
    if issues:
        print("\n[WARNING] Some dependencies are missing:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nThe app will still start, but some features may not work.")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 