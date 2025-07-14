#!/usr/bin/env python3
"""
Golf Ball Label Generator Web App Startup Script
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def check_node_dependencies():
    """Check if Node.js dependencies are installed."""
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    node_modules_path = os.path.join(web_app_dir, "node_modules")
    
    if not os.path.exists(node_modules_path):
        print("Installing Node.js dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=web_app_dir, check=True)
            print("Node.js dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Node.js dependencies: {e}")
            return False
    
    return True

def main():
    print("=== Golf Ball Label Generator Web App ===")
    print("Setting up the web application...")
    print()
    
    # Install Python dependencies
    if not install_dependencies():
        print("\nSetup failed. Please check the error messages above.")
        return
    
    # Check Node.js dependencies
    if not check_node_dependencies():
        print("\nNode.js dependencies not installed. The 3D viewer may not work.")
    
    print("\nSetup complete!")
    print("\nStarting the web application...")
    print("The app will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Start the web app
    try:
        subprocess.run([sys.executable, "web_app.py"])
    except KeyboardInterrupt:
        print("\nWeb app stopped.")

if __name__ == "__main__":
    main() 