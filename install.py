#!/usr/bin/env python3
"""
Installation script for ComfyUI Insightface Installer Node

This script helps with the initial setup and validation of the node.
It can be run after cloning the repository to ensure everything is working correctly.

Usage:
    python install.py
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is supported."""
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}"
    
    supported_versions = ["3.10", "3.11", "3.12"]
    
    print(f"🐍 Python version: {version_str}")
    
    if version_str in supported_versions:
        print("✅ Python version is supported")
        return True
    else:
        print(f"❌ Python version {version_str} is not supported")
        print(f"   Supported versions: {', '.join(supported_versions)}")
        return False

def check_comfyui_environment():
    """Check if we're in a ComfyUI environment."""
    current_path = Path(__file__).resolve()
    
    # Look for ComfyUI indicators
    for parent in current_path.parents:
        if (parent / "main.py").exists() and (parent / "comfy").exists():
            print(f"✅ ComfyUI installation detected at: {parent}")
            return True
    
    print("⚠️ ComfyUI installation not detected in parent directories")
    print("   Make sure this node is installed in ComfyUI/custom_nodes/")
    return False

def run_tests():
    """Run the node tests."""
    print("\n🧪 Running node tests...")
    
    try:
        # Import and run tests
        from test_node import main as run_tests
        run_tests()
        return True
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def check_file_structure():
    """Check if all required files are present."""
    print("\n📁 Checking file structure...")
    
    required_files = [
        "__init__.py",
        "insightface_installer.py",
        "README.md",
        "LICENSE",
        "requirements.txt"
    ]
    
    current_dir = Path(__file__).parent
    missing_files = []
    
    for file_name in required_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main installation and validation function."""
    print("🚀 ComfyUI Insightface Installer - Installation & Validation")
    print("=" * 70)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check file structure
    if not check_file_structure():
        success = False
    
    # Check ComfyUI environment
    if not check_comfyui_environment():
        print("⚠️ Warning: ComfyUI environment not detected, but node may still work")
    
    # Run tests
    if not run_tests():
        success = False
    
    print("\n" + "=" * 70)
    
    if success:
        print("🎉 Installation validation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart ComfyUI if it's currently running")
        print("2. Look for 'Insightface Installer' in the utilities/installation category")
        print("3. Configure your settings and run the workflow")
        print("\n💡 Tips:")
        print("- The node will auto-detect your ComfyUI installation type")
        print("- Choose the Python version that matches your current environment")
        print("- Use 'Force Reinstall' if you need to update an existing installation")
    else:
        print("❌ Installation validation failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure you're using Python 3.10, 3.11, or 3.12")
        print("2. Make sure all files are present in the node directory")
        print("3. Verify you're in a ComfyUI custom_nodes directory")
        print("4. Check the error messages above for specific issues")
        sys.exit(1)

if __name__ == "__main__":
    main()
