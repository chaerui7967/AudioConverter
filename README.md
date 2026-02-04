# AudioConverter

### Project Overview
> AudioConverter is a desktop utility designed for Windows users to quickly and easily switch between audio output devices. Built with Python and Qt6, it provides a seamless experience for managing your audio environment.

### Features
 - Real-time Device Listing: Automatically detects and displays all currently connected audio output devices.

  - Instant Switching: Change your active audio output device instantly without navigating through complex Windows settings.

  - Modern UI: Features a clean and intuitive user interface powered by Qt6.

### Tech Stack
  - Language: Python 3.10

  - UI Framework: Qt6 (PySide6/PyQt6)

  - Packaging: PyInstaller (Windows Executable)UI 

### System Requirements
  - OS: Windows 11(64-bit)

>⚠️ Note: This application is exclusively designed for Windows. macOS and Linux are currently not supported.

### Getting Started
1. Using the Executable (Recommended)
You can run the application without installing Python.

    1. Go to the Releases page.
    2. Download the latest AudioConverter.exe.
    3. Run the file to start managing your audio devices.

2. Running from Source
If you prefer to run the source code directly:
```bash
# Clone repository
git clone https://github.com/chaerui7967/AudioConverter.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Build Instructions
To build the standalone executable yourself using PyInstaller:
```bash
pyinstaller main.spec
```

### License
This project is licensed under the **MIT License**.

### Third-Party Credits
This application utilizes third-party software as follows:

* **NirCmd**: Created by Nir Sofer ([NirSoft](https://www.nirsoft.net/utils/nircmd.html)). 
    * NirCmd is released as freeware. It is redistributed in this project without any modification, in accordance with its license terms:
    > "You are allowed to freely distribute this utility... as long as you don't charge anything for this. If you distribute this utility, you must include all files in the distribution package, without any modification!"
* **Qt6 (PySide6)**: Licensed under LGPLv3.This project is licensed under the MIT License.