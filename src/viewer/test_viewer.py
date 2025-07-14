#!/usr/bin/env python3
"""
Test script to diagnose web viewer issues
"""

import os
import subprocess
import sys
import time
import requests

def check_node_installation():
    """Check if Node.js and npm are installed."""
    print("=== Checking Node.js Installation ===")
    
    try:
        # Check node version
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"Node.js version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Node.js not found. Please install Node.js from https://nodejs.org/")
        return False
    
    npm_path = None
    try:
        # Check npm version
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        print(f"npm version: {result.stdout.strip()}")
        npm_path = "npm"  # npm is in PATH
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: npm not found in PATH. Trying alternative locations...")
        
        # Try common npm locations on Windows
        possible_npm_paths = [
            r"C:\Program Files\nodejs\npm.cmd",
            r"C:\Program Files (x86)\nodejs\npm.cmd",
            os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
            os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps\npm.exe")
        ]
        
        for path in possible_npm_paths:
            if os.path.exists(path):
                print(f"Found npm at: {path}")
                npm_path = path
                break
        
        if not npm_path:
            print("ERROR: npm not found. Please ensure npm is installed with Node.js.")
            return False
    
    # Store npm path globally for use in other functions
    global NPM_PATH
    NPM_PATH = npm_path
    return True

def check_web_app_files():
    """Check if all required web app files exist."""
    print("\n=== Checking Web App Files ===")
    
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    required_files = [
        "package.json",
        "server.js",
        "public/index.html",
        "public/app.js"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(web_app_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if Node.js dependencies are installed."""
    print("\n=== Checking Dependencies ===")
    
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    node_modules_path = os.path.join(web_app_dir, "node_modules")
    
    if os.path.exists(node_modules_path):
        print("✓ node_modules directory exists")
        return True
    else:
        print("✗ node_modules directory missing")
        return False

def install_dependencies():
    """Install Node.js dependencies."""
    print("\n=== Installing Dependencies ===")
    
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    
    try:
        result = subprocess.run(
            [NPM_PATH, "install"], 
            cwd=web_app_dir, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e.stderr}")
        return False

def test_server_start():
    """Test starting the server manually."""
    print("\n=== Testing Server Start ===")
    
    web_app_dir = os.path.join(os.getcwd(), 'src/viewer/w3')
    
    # Try npm start first
    print("Trying npm start...")
    try:
        process = subprocess.Popen(
            [NPM_PATH, "start"], 
            cwd=web_app_dir, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait a bit
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ npm start is running")
            
            # Test connection
            try:
                response = requests.get("http://localhost:3000", timeout=5)
                if response.status_code == 200:
                    print("✓ Server is responding correctly")
                    process.terminate()
                    return True
                else:
                    print(f"✗ Server responded with status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"✗ Could not connect to server: {e}")
            
            process.terminate()
        else:
            print("✗ npm start failed")
            
            # Try direct node execution
            print("Trying direct node execution...")
            process = subprocess.Popen(
                ["node", "server.js"], 
                cwd=web_app_dir, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            
            if process.poll() is None:
                print("✓ node server.js is running")
                
                try:
                    response = requests.get("http://localhost:3000", timeout=5)
                    if response.status_code == 200:
                        print("✓ Server is responding correctly")
                        process.terminate()
                        return True
                    else:
                        print(f"✗ Server responded with status {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"✗ Could not connect to server: {e}")
                
                process.terminate()
            else:
                print("✗ node server.js also failed")
    
    except Exception as e:
        print(f"✗ Error starting server: {e}")
    
    return False

def main():
    """Main test function."""
    print("=== Web Viewer Diagnostic Tool ===")
    print()
    
    # Check Node.js installation
    if not check_node_installation():
        print("\nPlease install Node.js and npm before continuing.")
        return
    
    # Check web app files
    if not check_web_app_files():
        print("\nMissing required web app files. Please ensure the src/viewer/w3 directory is complete.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies.")
            return
    
    # Test server start
    if test_server_start():
        print("\n✓ Web viewer is working correctly!")
        print("You can access it at: http://localhost:3000")
    else:
        print("\n✗ Web viewer failed to start properly.")
        print("\nTroubleshooting tips:")
        print("1. Make sure no other application is using port 3000")
        print("2. Check if your firewall is blocking the connection")
        print("3. Try running 'npm start' manually in the src/viewer/w3 directory")
        print("4. Check the console output for specific error messages")

if __name__ == "__main__":
    main() 