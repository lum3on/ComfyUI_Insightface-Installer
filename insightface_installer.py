"""
ComfyUI Insightface Installer Node

A ComfyUI custom node for installing the correct Insightface wheel based on Python version.
Supports both regular and portable ComfyUI installations.

Author: ComfyUI Node Architect
Version: 1.0.0
"""

import os
import sys
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
import platform
import json
from typing import Tuple, Optional

class InsightfaceInstaller:
    """
    ComfyUI node for installing Insightface wheels based on Python version.
    
    This node provides a user-friendly interface to download and install
    the correct Insightface wheel for the current Python environment,
    supporting both regular and portable ComfyUI installations.
    """
    
    # Wheel URLs for different Python versions
    WHEEL_URLS = {
        "3.10": "https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp310-cp310-win_amd64.whl",
        "3.11": "https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp311-cp311-win_amd64.whl", 
        "3.12": "https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp312-cp312-win_amd64.whl"
    }
    
    # Wheel filenames for different Python versions
    WHEEL_FILENAMES = {
        "3.10": "insightface-0.7.3-cp310-cp310-win_amd64.whl",
        "3.11": "insightface-0.7.3-cp311-cp311-win_amd64.whl",
        "3.12": "insightface-0.7.3-cp312-cp312-win_amd64.whl"
    }

    @staticmethod
    def _detect_installation_type():
        """
        Detect whether we're in a portable or regular ComfyUI installation.

        Returns:
            str: "Portable ComfyUI" if portable installation detected, "Regular ComfyUI" otherwise
        """
        try:
            # Find ComfyUI root directory
            current_path = Path(__file__).resolve()

            # Look for ComfyUI root indicators
            comfyui_root = None
            for parent in current_path.parents:
                if (parent / "main.py").exists() and (parent / "comfy").exists():
                    comfyui_root = parent
                    break

            # Fallback: assume we're in custom_nodes and go up two levels
            if comfyui_root is None and "custom_nodes" in str(current_path):
                for parent in current_path.parents:
                    if parent.name == "custom_nodes":
                        comfyui_root = parent.parent
                        break

            # Last resort: use current working directory
            if comfyui_root is None:
                comfyui_root = Path.cwd()

            # Check for portable installation indicators
            python_embeded_path = comfyui_root.parent / "python_embeded"
            if python_embeded_path.exists() and python_embeded_path.is_dir():
                print(f"🔍 Auto-detected: Portable ComfyUI installation (found python_embeded at {python_embeded_path})")
                return "Portable ComfyUI"
            else:
                print(f"🔍 Auto-detected: Regular ComfyUI installation (no python_embeded found)")
                return "Regular ComfyUI"

        except Exception as e:
            print(f"⚠️ Warning: Could not auto-detect installation type ({e}), defaulting to Regular ComfyUI")
            return "Regular ComfyUI"

    @classmethod
    def INPUT_TYPES(s):
        """
        Define the input types for the node.

        Returns:
            Dict containing the input specifications for ComfyUI
        """
        # Auto-detect installation type for default value
        detected_type = s._detect_installation_type()

        return {
            "required": {
                "python_version": (["3.10", "3.11", "3.12"], {
                    "default": "3.11"
                }),
                "installation_type": (["Regular ComfyUI", "Portable ComfyUI"], {
                    "default": detected_type
                }),
                "force_reinstall": ("BOOLEAN", {
                    "default": False
                })
            },
            "optional": {
                "animated_background": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Animated BG",
                    "label_off": "Static BG"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("installation_status",)
    FUNCTION = "install_insightface"
    CATEGORY = "utilities/installation"
    DESCRIPTION = "Install Insightface wheel for the selected Python version"

    # Additional ComfyUI attributes for better compatibility
    OUTPUT_NODE = False
    DEPRECATED = False

    def __init__(self):
        """Initialize the installer node."""
        self.comfyui_root = self._find_comfyui_root()
        
    def _find_comfyui_root(self) -> Path:
        """
        Find the ComfyUI root directory.
        
        Returns:
            Path to the ComfyUI root directory
        """
        # Start from current file location and traverse up
        current_path = Path(__file__).resolve()
        
        # Look for ComfyUI root indicators
        for parent in current_path.parents:
            if (parent / "main.py").exists() and (parent / "comfy").exists():
                return parent
                
        # Fallback: assume we're in custom_nodes and go up two levels
        if "custom_nodes" in str(current_path):
            for parent in current_path.parents:
                if parent.name == "custom_nodes":
                    return parent.parent
                    
        # Last resort: use current working directory
        return Path.cwd()

    def _get_current_python_version(self) -> str:
        """
        Get the current Python version in X.Y format.
        
        Returns:
            Python version string (e.g., "3.11")
        """
        version_info = sys.version_info
        return f"{version_info.major}.{version_info.minor}"

    def _download_wheel(self, python_version: str, download_path: Path) -> Tuple[bool, str]:
        """
        Download the Insightface wheel for the specified Python version.
        
        Args:
            python_version: Python version (e.g., "3.11")
            download_path: Path where to save the wheel file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if python_version not in self.WHEEL_URLS:
            return False, f"Unsupported Python version: {python_version}"
            
        url = self.WHEEL_URLS[python_version]
        filename = self.WHEEL_FILENAMES[python_version]
        file_path = download_path / filename
        
        try:
            # Create download directory if it doesn't exist
            download_path.mkdir(parents=True, exist_ok=True)
            
            # Check if file already exists
            if file_path.exists():
                return True, f"Wheel file already exists: {file_path}"
            
            print(f"Downloading {filename} from {url}...")
            
            # Download with progress indication
            def progress_hook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = min(100, (block_num * block_size * 100) // total_size)
                    print(f"\rDownload progress: {percent}%", end="", flush=True)
            
            urllib.request.urlretrieve(url, file_path, reporthook=progress_hook)
            print()  # New line after progress
            
            return True, f"Successfully downloaded: {file_path}"
            
        except urllib.error.URLError as e:
            return False, f"Download failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during download: {str(e)}"

    def _install_wheel(self, wheel_path: Path, installation_type: str, force_reinstall: bool) -> Tuple[bool, str]:
        """
        Install the downloaded wheel using the appropriate method.
        
        Args:
            wheel_path: Path to the wheel file
            installation_type: "Regular ComfyUI" or "Portable ComfyUI"
            force_reinstall: Whether to force reinstallation
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if installation_type == "Portable ComfyUI":
                # Use python_embedded for portable installation
                python_embedded_path = self.comfyui_root.parent / "python_embeded" / "python.exe"
                
                if not python_embedded_path.exists():
                    return False, f"Python embedded not found at: {python_embedded_path}"
                
                cmd = [str(python_embedded_path), "-m", "pip", "install"]
            else:
                # Use regular pip for standard installation
                cmd = [sys.executable, "-m", "pip", "install"]
            
            # Add force reinstall flag if requested
            if force_reinstall:
                cmd.extend(["--force-reinstall"])
            
            # Add the wheel file path
            cmd.append(str(wheel_path))
            
            print(f"Installing with command: {' '.join(cmd)}")
            
            # Execute the installation command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.comfyui_root)
            )
            
            if result.returncode == 0:
                return True, f"Successfully installed Insightface wheel: {wheel_path.name}"
            else:
                error_msg = result.stderr or result.stdout or "Unknown installation error"
                return False, f"Installation failed: {error_msg}"
                
        except Exception as e:
            return False, f"Installation error: {str(e)}"

    def install_insightface(self, python_version: str, installation_type: str, force_reinstall: bool, animated_background: bool = True) -> Tuple[str]:
        """
        Main function to download and install Insightface wheel.
        
        Args:
            python_version: Selected Python version
            installation_type: Installation method
            force_reinstall: Whether to force reinstallation
            animated_background: UI toggle, not used in logic
            
        Returns:
            Tuple containing installation status message
        """
        try:
            # Validate inputs
            if python_version not in self.WHEEL_URLS:
                return (f"❌ Error: Unsupported Python version '{python_version}'",)
            
            # Get current Python version for validation
            current_version = self._get_current_python_version()
            if python_version != current_version:
                warning_msg = f"⚠️ Warning: Selected version {python_version} differs from current Python {current_version}"
                print(warning_msg)
            
            # Set download path to ComfyUI root
            download_path = self.comfyui_root
            
            print(f"ComfyUI root directory: {self.comfyui_root}")
            print(f"Installing Insightface for Python {python_version}")
            print(f"Installation type: {installation_type}")

            # Show detection info if using auto-detected type
            detected_type = self._detect_installation_type()
            if installation_type == detected_type:
                print(f"✅ Using auto-detected installation type: {installation_type}")
            else:
                print(f"⚠️ Manual override: detected {detected_type}, but using {installation_type}")
            
            # Download the wheel
            download_success, download_msg = self._download_wheel(python_version, download_path)
            if not download_success:
                return (f"❌ Download failed: {download_msg}",)
            
            print(download_msg)
            
            # Get wheel file path
            wheel_filename = self.WHEEL_FILENAMES[python_version]
            wheel_path = download_path / wheel_filename
            
            if not wheel_path.exists():
                return (f"❌ Error: Wheel file not found after download: {wheel_path}",)
            
            # Install the wheel
            install_success, install_msg = self._install_wheel(wheel_path, installation_type, force_reinstall)
            
            if install_success:
                status_msg = f"✅ {install_msg}"
                if python_version != current_version:
                    status_msg += f"\n⚠️ Note: Installed for Python {python_version}, but current version is {current_version}"
                return (status_msg,)
            else:
                return (f"❌ Installation failed: {install_msg}",)
                
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            print(error_msg)
            return (error_msg,)

# Node registration mapping
NODE_CLASS_MAPPINGS = {
    "InsightfaceInstaller": InsightfaceInstaller
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "InsightfaceInstaller": "🌿 𝓘𝓷𝓼𝓲𝓰𝓱𝓽𝓯𝓪𝓬𝓮 𝓘𝓷𝓼𝓽𝓪𝓵𝓵𝓮𝓻 🌿"
}
