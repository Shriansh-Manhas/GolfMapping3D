#!/usr/bin/env python3
"""
Script to help fix npm PATH issues on Windows
"""

import os
import subprocess
import sys

def find_npm():
    """Find where npm is installed."""
    print("=== Finding npm installation ===")
    
    # Common npm locations on Windows
    possible_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
        os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps\npm.exe"),
        r"C:\Program Files\nodejs\npm.exe",
        r"C:\Program Files (x86)\nodejs\npm.exe"
    ]
    
    found_paths = []
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found npm at: {path}")
            found_paths.append(path)
        else:
            print(f"✗ Not found: {path}")
    
    return found_paths

def check_path():
    """Check current PATH for npm."""
    print("\n=== Checking PATH ===")
    
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    
    npm_in_path = False
    for directory in path_dirs:
        npm_path = os.path.join(directory, 'npm.cmd')
        npm_exe = os.path.join(directory, 'npm.exe')
        if os.path.exists(npm_path) or os.path.exists(npm_exe):
            print(f"✓ npm found in PATH: {directory}")
            npm_in_path = True
    
    if not npm_in_path:
        print("✗ npm not found in PATH")
    
    return npm_in_path

def test_npm_commands():
    """Test npm commands."""
    print("\n=== Testing npm commands ===")
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        print(f"✓ npm --version works: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ npm --version failed")
        return False

def suggest_fix():
    """Suggest how to fix the PATH issue."""
    print("\n=== Suggested Fix ===")
    
    npm_paths = find_npm()
    
    if npm_paths:
        print("\nTo fix this issue, add one of these directories to your PATH:")
        for path in npm_paths:
            directory = os.path.dirname(path)
            print(f"  {directory}")
        
        print("\nYou can do this by:")
        print("1. Opening System Properties (Win + Pause/Break)")
        print("2. Click 'Environment Variables'")
        print("3. Under 'System Variables', find 'Path' and click 'Edit'")
        print("4. Click 'New' and add one of the directories above")
        print("5. Click 'OK' on all dialogs")
        print("6. Restart your command prompt/terminal")
        
        print("\nOr you can run this command in PowerShell as Administrator:")
        for path in npm_paths:
            directory = os.path.dirname(path)
            print(f'  [Environment]::SetEnvironmentVariable("Path", $env:Path + ";{directory}", "Machine")')
    else:
        print("No npm installation found. Please install Node.js from https://nodejs.org/")

def main():
    """Main function."""
    print("=== npm PATH Fix Tool ===")
    print()
    
    # Check if npm is in PATH
    npm_in_path = check_path()
    
    # Test npm command
    npm_works = test_npm_commands()
    
    if npm_works:
        print("\n✓ npm is working correctly!")
        return
    
    # Find npm installations
    npm_paths = find_npm()
    
    if npm_paths:
        print(f"\nFound {len(npm_paths)} npm installation(s) but they're not in PATH.")
        suggest_fix()
    else:
        print("\nNo npm installation found. Please install Node.js from https://nodejs.org/")

if __name__ == "__main__":
    main() 