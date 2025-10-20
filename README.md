# ComfyUI Insightface Installer
^
<img width="1325" height="942" alt="image" src="https://github.com/user-attachments/assets/d4a4feac-c86e-41db-872c-32c920f63c1f" />

A ComfyUI custom node that provides an easy-to-use interface for installing the correct Insightface wheel based on your Python version and ComfyUI installation type.

## Features

- 🐍 **Multi-Python Support**: Supports Python 3.10, 3.11, 3.12, and 3.13
- 🔧 **Auto-Detection**: Automatically detects portable vs regular ComfyUI installations
- 📦 **Automatic Downloads**: Downloads wheels directly to your ComfyUI root directory
- ⚡ **Smart Detection**: Automatically detects your ComfyUI root directory
- 🛡️ **Robust Error Handling**: Comprehensive error handling with clear user feedback
- 🔄 **Force Reinstall**: Option to force reinstallation if needed

## Installation

### Method 1: Git Clone (Recommended)

1. Navigate to your ComfyUI custom_nodes directory:
   ```bash
   cd ComfyUI/custom_nodes
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ComfyUI-Insightface-Installer.git
   ```

3. Restart ComfyUI

### Method 2: Manual Installation

1. Download this repository as a ZIP file
2. Extract it to your `ComfyUI/custom_nodes/` directory
3. Ensure the folder is named `ComfyUI-Insightface-Installer`
4. Restart ComfyUI

## Usage

1. **Add the Node**: In ComfyUI, add the "Insightface Installer" node from the `utilities/installation` category

2. **Configure Settings**:
   - **Python Version**: Select your Python version (3.10, 3.11, 3.12, or 3.13)
   - **Installation Type**: Auto-detected (Portable/Regular), but can be manually overridden if needed
   - **Force Reinstall**: Enable if you want to reinstall even if Insightface is already present

3. **Execute**: Run the workflow to download and install the Insightface wheel

## Supported Wheels

The node automatically downloads the appropriate wheel from the official Gourieff Assets repository:

- **Python 3.10**: `insightface-0.7.3-cp310-cp310-win_amd64.whl`
- **Python 3.11**: `insightface-0.7.3-cp311-cp311-win_amd64.whl`
- **Python 3.12**: `insightface-0.7.3-cp312-cp312-win_amd64.whl`
- **Python 3.13**: `insightface-0.7.3-cp313-cp313-win_amd64.whl`

## Installation Types

### Regular ComfyUI
Uses the standard pip installation method:
```bash
pip install insightface-0.7.3-cp311-cp311-win_amd64.whl
```

### Portable ComfyUI
Uses the embedded Python installation:
```bash
python_embeded\python.exe -m pip install insightface-0.7.3-cp311-cp311-win_amd64.whl
```

## Output

The node returns a status message indicating:
- ✅ Successful installation
- ❌ Error details if installation fails
- ⚠️ Warnings for version mismatches

## Troubleshooting

### Common Issues

1. **"Python embedded not found"**
   - The installer should auto-detect your installation type, but you can manually override if needed
   - If you have a portable installation, ensure the `python_embeded` folder exists in your ComfyUI root
   - If auto-detection fails, manually select "Regular ComfyUI" for standard installations

2. **"Download failed"**
   - Check your internet connection
   - Verify the wheel URLs are accessible
   - Try again after a few minutes

3. **"Installation failed"**
   - Check if you have write permissions to the ComfyUI directory
   - Try running ComfyUI as administrator (Windows)
   - Enable "Force Reinstall" if Insightface is already installed

### Version Mismatch Warning

If you see a warning about version mismatch, it means:
- You selected a different Python version than what's currently running
- The wheel will still be downloaded and installation attempted
- For best compatibility, select the version matching your current Python installation

## Technical Details

### Directory Structure
```
ComfyUI-Insightface-Installer/
├── __init__.py                 # Node registration
├── insightface_installer.py    # Main node implementation
├── README.md                   # This file
└── state/                      # ComfyUI state files
```

### Dependencies
- Python 3.10, 3.11, 3.12, or 3.13
- ComfyUI
- Internet connection for downloading wheels

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure you're using a supported Python version
3. Verify your ComfyUI installation is working correctly
4. Open an issue on GitHub with detailed error messages

## Credits

- Insightface wheels provided by [Gourieff](https://github.com/Gourieff/Assets)
- Built for the ComfyUI community

---

**Note**: This node is specifically designed for Windows AMD64 architecture. Linux and other architectures may require different wheel files.
