# PyPixPro

```
██████╗ ██╗   ██╗██████╗ ██╗██╗  ██╗██████╗ ██████╗  ██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██║╚██╗██╔╝██╔══██╗██╔══██╗██╔═══██╗
██████╔╝ ╚████╔╝ ██████╔╝██║ ╚███╔╝ ██████╔╝██████╔╝██║   ██║
██╔═══╝   ╚██╔╝  ██╔═══╝ ██║ ██╔██╗ ██╔═══╝ ██╔══██╗██║   ██║
██║        ██║   ██║     ██║██╔╝ ██╗██║     ██║  ██║╚██████╔╝
╚═╝        ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
```

## PyPixPro — Intelligent Photo Organization for macOS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### ⚡ About

PyPixPro is a native macOS application that automatically organizes your photo library with intelligent sorting, duplicate detection, and batch renaming. Simply drag and drop a folder, and PyPixPro handles the rest.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### ✨ Highlights

- 🖼️ **Smart Orientation Sorting** – Automatically separates Portrait and Landscape photos
- 🧬 **Zero Duplicates** – BLAKE3 hashing detects and removes duplicate files instantly
- 📱 **HEIC/HEIF Support** – Full support for iPhone ProRAW and HEIC formats
- 📸 **Screenshot Detection** – PNG files automatically sorted to Screenshots folder
- 🎞️ **GIF & WebP Handling** – Animated content gets its own dedicated folder
- 📷 **ProRAW Support** – DNG, RAW, NEF, CR2, CR3, ARW and more
- ✏️ **Smart Renaming** – Batch rename with custom prefixes (Portrait V 001, Landscape W 001)
- 💾 **Automatic Backup** – Creates backup on Desktop before any changes
- 📊 **Real-Time Logging** – Live progress with detailed summary table
- 🖥️ **Apple Silicon Native** – Optimized for M1/M2/M3/M4 chips

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🎯 Supported Formats

| Category | Formats |
|----------|---------|
| **Standard Images** | JPG, JPEG, BMP, TIFF, TIF, PSD, SVG, ICO, JFIF, AVIF, APNG |
| **Apple Formats** | HEIC, HEIF |
| **Animated** | GIF, WebP |
| **Screenshots** | PNG |
| **RAW/ProRAW** | DNG, RAW, NEF, CR2, CR3, ARW, ORF, RW2, RAF, SRW, KDC |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📦 Installation

1. Download the latest `PyPixPro.dmg` from [Releases](https://github.com/RazorBackRoar/PyPixPro/releases)
2. Mount the DMG → drag `PyPixPro.app` into `/Applications` → eject
3. First launch (Gatekeeper):

   - **Method A:** Right-click `PyPixPro.app` → _Open_ → confirm
   - **Method B:**

     ```bash
     sudo xattr -cr /Applications/PyPixPro.app
     ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🚀 Usage

1. Launch PyPixPro
2. **Drag and drop** any folder onto the window
3. Enter custom prefixes for Portrait/Landscape files (or use defaults)
4. Watch the real-time log as files are processed
5. Check your Desktop for the backup folder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📁 Output Structure

```text
YourFolder/
├── Portrait/           # Vertical images (height > width)
│   ├── MyPrefix V 001.jpg
│   ├── MyPrefix V 002.heic
│   └── ...
├── Landscape/          # Horizontal images (width >= height)
│   ├── MyPrefix W 001.jpg
│   └── ...
├── Screenshots/        # All PNG files
│   └── screenshot.png
├── GIF/                # Animated content
│   ├── animation.gif
│   └── sticker.webp
├── ProRaw/             # RAW camera files
│   ├── photo.dng
│   └── image.cr3
└── Random/             # Unrecognized file types
    └── document.pdf
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 💻 Requirements

- macOS 10.13+
- ~100 MB free disk space
- No Python install needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔧 Troubleshooting

- **"App is damaged / Cannot be opened"** – Use the Gatekeeper override above
- **HEIC files not processing** – Ensure you have the latest version with pillow-heif
- **Files not moving** – Check folder permissions and ensure backup completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🛠️ Building from Source

```bash
# Clone repository
git clone https://github.com/RazorBackRoar/PyPixPro.git
cd PyPixPro

# Install dependencies
pip install -r requirements.txt

# Run from source
python src/pypixpro/main.py

# Build app bundle
pyinstaller build/PyPixPro.spec
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📜 License

MIT License – see `LICENSE`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🐞 Support

- Issues: <https://github.com/RazorBackRoar/PyPixPro/issues>
- Source: <https://github.com/RazorBackRoar/PyPixPro>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔐 Privacy

PyPixPro runs 100% locally. No telemetry, no analytics, no network calls. Your photos stay on your machine.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 👤 Author

**RazorBackRoar**

GitHub: [@RazorBackRoar](https://github.com/RazorBackRoar)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
