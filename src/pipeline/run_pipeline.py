import subprocess
import time
import os
import sys
import asyncio
import threading
from pathlib import Path

# --- CONFIG ---
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../../assets/images/image.png')
GLB_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../../assets/models/exported_label.glb')
BLEND_FILE = os.path.join(os.path.dirname(__file__), '../../assets/blend_files/Golf.blend')
BLENDER_DIR = r"C:\Program Files\Blender Foundation\Blender 4.4"
BLENDER_EXE = os.path.join(BLENDER_DIR, "blender.exe")

def check_dependencies():
    """Check if all required files and dependencies exist."""
    print("=== Checking Dependencies ===")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("[ERROR] .env file not found! Please create it with your OpenAI API key.")
        return False
    
    # Check if Blender exists
    if not os.path.exists(BLENDER_EXE):
        print(f"[ERROR] Blender not found at: {BLENDER_EXE}")
        print("Please update BLENDER_DIR in the script to your Blender installation path.")
        return False
    
    # Check if .blend file exists
    if not os.path.exists(BLEND_FILE):
        print(f"[ERROR] Blender file not found: {BLEND_FILE}")
        return False
    
    # Check if required Python scripts exist
    required_scripts = [os.path.join(os.path.dirname(__file__), '../../scripts/generate_image_with_dalle.py'), os.path.join(os.path.dirname(__file__), '../blender/generate_label_glb.py')]
    for script in required_scripts:
        if not os.path.exists(script):
            print(f"[ERROR] Required script not found: {script}")
            return False
    
    # Check if web app directory exists
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    if not os.path.exists(web_app_dir):
        print(f"[ERROR] Web app directory not found: {web_app_dir}")
        return False
    
    # Check if web app files exist
    required_web_files = ["server.js", "package.json", "public/index.html", "public/app.js"]
    for file in required_web_files:
        file_path = os.path.join(web_app_dir, file)
        if not os.path.exists(file_path):
            print(f"[ERROR] Required web app file not found: {file_path}")
            return False
    
    print("[SUCCESS] All dependencies found!")
    return True

def run_dalle_generation(prompt=None):
    """Run DALL-E image generation."""
    print("\n=== Step 1: Generating Image with DALL-E ===")
    
    try:
        if prompt:
            # Run with custom prompt
            result = subprocess.run([
                sys.executable, os.path.join(os.path.dirname(__file__), '../../scripts/generate_image_with_dalle.py'), '--prompt', prompt
            ], capture_output=True, text=True, check=True)
        else:
            # Run with interactive prompt
            result = subprocess.run([
                sys.executable, os.path.join(os.path.dirname(__file__), '../../scripts/generate_image_with_dalle.py')
            ], capture_output=True, text=True, check=True)
        
        print("[SUCCESS] Image generated successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] DALL-E generation failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def run_blender_export():
    """Run Blender export process."""
    print("\n=== Step 2: Updating 3D Model in Blender ===")
    
    try:
        command = [
            BLENDER_EXE, BLEND_FILE,
            "--background",
            "--python", os.path.join(os.path.dirname(__file__), '../blender/generate_label_glb.py'),
            "--", IMAGE_PATH, GLB_OUTPUT_PATH
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("[SUCCESS] 3D model updated and exported!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Blender export failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def display_glb_file():
    """Display the generated GLB file using the web app."""
    print("\n=== Step 3: Displaying GLB File ===")
    
    if not os.path.exists(GLB_OUTPUT_PATH):
        print(f"[ERROR] GLB file not found: {GLB_OUTPUT_PATH}")
        return False
    
    print(f"[INFO] GLB file generated: {GLB_OUTPUT_PATH}")
    print(f"[INFO] File size: {os.path.getsize(GLB_OUTPUT_PATH) / 1024:.1f} KB")
    
    # Start the web app server
    try:
        import subprocess
        import webbrowser
        import time
        
        # Check if web app directory exists
        web_app_dir = os.path.join(os.getcwd(), "src/viewer/w3")
        if not os.path.exists(web_app_dir):
            print(f"[ERROR] Web app directory not found: {web_app_dir}")
            return False
        
        # Check if node_modules exists, if not install dependencies
        node_modules_path = os.path.join(web_app_dir, "node_modules")
        if not os.path.exists(node_modules_path):
            print("[INFO] Installing web app dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=web_app_dir, check=True, capture_output=True)
                print("[SUCCESS] Dependencies installed!")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to install dependencies: {e}")
                return False
        
        # Start the server
        print("[INFO] Starting web app server...")
        try:
            # Try using npm start first
            server_process = subprocess.Popen(
                ["npm", "start"], 
                cwd=web_app_dir, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            # Fallback to direct node execution
            print("[INFO] npm not found, trying direct node execution...")
            server_process = subprocess.Popen(
                ["node", "server.js"], 
                cwd=web_app_dir, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("[SUCCESS] Server is running!")
            else:
                print(f"[WARN] Server responded with status {response.status_code}")
        except ImportError:
            print("[INFO] requests module not available, skipping server check")
        except Exception as e:
            print(f"[WARN] Could not verify server status: {e}")
        
        # Open browser
        webbrowser.open("http://localhost:3000")
        print("[SUCCESS] Web app opened in browser!")
        print("[INFO] The 3D model should load automatically")
        print("[INFO] Server is running on http://localhost:3000")
        print("[INFO] Press Ctrl+C in the terminal to stop the server")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to start web app: {e}")
        
        # Fallback to default application
        try:
            os.startfile(GLB_OUTPUT_PATH)
            print("[SUCCESS] GLB file opened with default application!")
            return True
        except Exception as e2:
            print(f"[WARN] Could not open GLB file automatically: {e2}")
            print(f"[INFO] You can manually open: {GLB_OUTPUT_PATH}")
            return False

def main():
    """Main pipeline function."""
    print("=== Golf Label 3D Pipeline ===")
    print("This will: Generate image -> Update 3D model -> Display result")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n[ERROR] Dependencies check failed. Please fix the issues above.")
        return
    
    # Get custom prompt if desired
    use_custom_prompt = input("Use custom prompt? (y/n, default: n): ").strip().lower()
    custom_prompt = None
    
    if use_custom_prompt == 'y':
        custom_prompt = input("Enter your custom prompt: ").strip()
        if not custom_prompt:
            print("[INFO] Using default prompt.")
            custom_prompt = None
    
    # Step 1: Generate image
    if not run_dalle_generation(custom_prompt):
        print("\n[ERROR] Pipeline failed at image generation step.")
        return
    
    # Step 2: Update 3D model
    if not run_blender_export():
        print("\n[ERROR] Pipeline failed at 3D model update step.")
        return
    
    # Step 3: Display result
    display_glb_file()
    
    print("\n=== Pipeline Complete! ===")
    print("Your 3D golf ball model has been updated with the new label design.")
    print(f"GLB file location: {GLB_OUTPUT_PATH}")

if __name__ == "__main__":
    main() 