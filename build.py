"""
Build script for TaskManager
Creates a standalone executable for distribution.

Usage:
    python build.py
"""

import subprocess
import sys
import shutil
from pathlib import Path

def main():
    print("=" * 50)
    print("TaskManager Build Script")
    print("=" * 50)
    
    # Check for PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Build configuration
    app_name = "TaskManager"
    main_script = "main.py"
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Single executable
        "--windowed",          # No console window
        "--name", app_name,    # Output name
        "--clean",             # Clean cache before building
        main_script
    ]
    
    # Optional: Add icon if it exists
    icon_path = Path("icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"✓ Using icon: {icon_path}")
    
    print(f"\nBuilding {app_name}...")
    print("-" * 50)
    
    # Run PyInstaller
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = Path("dist") / f"{app_name}.exe"
        print("-" * 50)
        print(f"✓ Build successful!")
        print(f"✓ Executable: {exe_path.absolute()}")
        print(f"✓ Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        print("\nTo distribute:")
        print(f"  1. Share: dist\\{app_name}.exe")
        print("  2. tasks.json will be created automatically on first run")
    else:
        print(f"✗ Build failed with exit code {result.returncode}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
