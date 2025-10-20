"""
ComfyUI Insightface Installer - Custom Node Package

This package provides a ComfyUI custom node for installing Insightface wheels
based on the Python version and installation type (regular vs portable).

Features:
- Automatic Python version detection
- Support for Python 3.10, 3.11, 3.12, and 3.13
- Handles both regular and portable ComfyUI installations
- Downloads wheels directly to ComfyUI root directory
- Robust error handling and user feedback

Author: ComfyUI Node Architect
Version: 1.0.0
License: MIT
"""

# Import the node classes and mappings
# This structure allows for cleaner management of multiple nodes.
from .insightface_installer import InsightfaceInstaller

# A dictionary that maps class names to class objects
NODE_CLASS_MAPPINGS = {
    "InsightfaceInstaller": InsightfaceInstaller
}

# A dictionary that maps class names to their display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "InsightfaceInstaller": "🌿 𝓘𝓷𝓼𝓲𝓰𝓱𝓽𝓯𝓪𝓬𝓮 𝓘𝓷𝓼𝓽𝓪𝓵𝓵𝓮𝓻 🌿"
}

# Define the web directory for any front-end extensions
WEB_DIRECTORY = "./web"

# Export the mappings that ComfyUI needs to recognize the custom node
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]


# Versioning and metadata
__version__ = "1.1.0" # Incremented version
__author__ = "ComfyUI Node Architect"
__description__ = "A robust installer for Insightface with a custom UI."
