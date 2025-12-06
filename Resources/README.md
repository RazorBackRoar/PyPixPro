# PyPixPro

PyPixPro is an automated image sorting and renaming tool for macOS. It leverages Python’s powerful libraries to sort images based on orientation, correct image metadata, and organize your folders efficiently. This tool supports multiple file types, including JPEG, PNG, HEIC, and raw image formats, and it even generates checksums for verification.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [How It Works](#how-it-works)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [File Types Supported](#file-types-supported)  
7. [Advanced Configuration](#advanced-configuration)  
8. [Troubleshooting](#troubleshooting)  
9. [Contributing](#contributing)  
10. [License](#license)  
11. [Contact](#contact)  

---

## Overview

PyPixPro simplifies the process of managing and sorting images. It organizes photos into Portrait and Landscape folders, handles HEIC files, generates checksums, and renames files with customizable prefixes. This tool aims to keep your photo library neat, with minimal manual intervention.

---

## Features

- **Automated Sorting**: Categorize images into Portrait, Landscape, Screenshots, or Misc folders.  
- **Metadata Correction**: Fix image orientation using EXIF metadata.  
- **HEIC Support**: Process HEIC and HEIF images seamlessly.  
- **Checksum Generation**: Verify file integrity using SHA-256 checksums.  
- **Custom Prefixes**: Rename files with user-defined prefixes for better organization.  
- **Cross-format Handling**: Sorts raw images, videos, and even documents.  
- **Error Handling**: Continues processing even if some files encounter errors.  
- **macOS Integration**: Uses `osascript` for user prompts and alerts.

---

## How It Works

1. **Input Folder Selection**: The user provides a folder via drag-and-drop or command-line input.
2. **Checksum Generation**: SHA-256 checksums are generated to ensure data integrity.
3. **Sorting Process**:
   - **Portrait vs. Landscape**: Images are sorted based on their orientation.
   - **Screenshots & Miscellaneous Files**: Specific file types are moved to dedicated folders.
4. **File Renaming**: Files in the Portrait and Landscape folders are renamed with custom prefixes.
5. **Completion Alert**: A macOS alert notifies the user when the process finishes.

---

## Installation

1. **Install Python 3** (if not already installed).  
   - Use Homebrew:  
     ```bash
     brew install python
     ```

2. **Install Dependencies**:  
   ```bash
   pip install pillow pyheif
   ```

---

## Usage

### Basic Usage

1. **Drag and Drop**: Drop a folder onto the PyPixPro droplet to start the process.  
2. **Command-Line Usage**:
   ```bash
   python3 PyPixPro.py /path/to/your/folder
   ```

---

## File Types Supported

- **Standard Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, etc.  
- **HEIC/HEIF Files**: `.heic`, `.heif`  
- **Raw Image Formats**: `.dng`, `.nef`, `.cr2`, `.arw`, etc.  
- **Miscellaneous Files**: `.txt`, `.pdf`, `.mp4`, `.mov`, etc.  

---

## Advanced Configuration

- **Modify Folder Names**: Adjust the constants in the code to change folder names.  
- **Add New File Types**: Extend supported file types by editing the `STANDARD_IMAGE_EXTENSIONS` or `MISC_EXTENSIONS` constants.  
- **Error Handling**: The script gracefully skips files with issues, printing errors for reference.

---

## Troubleshooting

- **HEIC Files Not Processed**: Ensure `pyheif` is installed via pip.  
- **Permission Errors**: Check if you have the necessary permissions for the input folder.  
- **EXIF Metadata Issues**: Some images might not contain correct orientation metadata.  
- **Slow Performance**: This can happen with large datasets—try excluding large files.

---

## Contributing

We welcome contributions to improve PyPixPro! Here’s how you can help:

1. **Fork the Repository** on GitHub.  
2. **Create a Feature Branch**:  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit Your Changes**:  
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. **Push to the Branch**:  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**: Submit your changes for review.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE.md](LICENSE.md) file for more information.

---

## Contact

Your Name – [RazorBackRoar@icloud.com](mailto:RazorBackRoar@icloud.com)  
Project Link: [GitHub](https://github.com/RazorBackRoar/PyPixPro)
