#!/usr/bin/env zsh
# Set project path
PROJECT_PATH="/Users/home/Scripts/GitHub/PyPixPro"
# Ask user if they want to proceed
echo "This will build PyPixPro for macOS. Continue? (y/n)"
read -q response
echo # new line
[[ $response == "n" ]] && exit 0
# Set error handling
set -e
# Function to check command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is required but not installed."
        echo "Install it? (y/n)"
        read -q response
        echo
        if [[ $response == "y" ]]; then
            brew install $1
        else
            exit 1
        fi
    fi
}
# Check required commands
check_command create-dmg
# Main build process
{
    # 1. Clean up
    cd "${PROJECT_PATH}"
    rm -rf build dist
    rm -f PyPixPro.spec
    # 2. Create spec file
    cat > PyPixPro.spec << 'EOL'
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(
    ['PyPixPro.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources/nxx.png', 'resources'),
        ('resources/nx.icns', 'resources')
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'Qt3DAnimation',
        'QtQuick',
        'QtWebView',
        'QtDBus'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PyPixPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/nx.icns'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyPixPro'
)
app = BUNDLE(
    coll,
    name='PyPixPro.app',
    icon='resources/nx.icns',
    bundle_identifier='com.PyPixPro.app',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '10.13.0',
    }
)
EOL
    echo "🔨 Building app..."
    /Users/home/miniforge3/bin/python3 -m PyInstaller --clean PyPixPro.spec
    echo "📝 Signing app..."
    cd dist
    codesign --force --deep --sign - PyPixPro.app
    echo "💿 Creating DMG..."
    create-dmg \
      --volname "PyPixPro" \
      --volicon "../resources/nx.icns" \
      --window-pos 200 120 \
      --window-size 600 300 \
      --icon-size 100 \
      --icon "PyPixPro.app" 175 120 \
      --hide-extension "PyPixPro.app" \
      --app-drop-link 425 120 \
      "PyPixPro.dmg" \
      "PyPixPro.app"
    echo "📝 Signing DMG..."
    codesign --force --sign - PyPixPro.dmg
    # Verify signatures
    echo "\n🔍 Verifying signatures..."
    codesign -v PyPixPro.app && echo "✅ App signature verified"
    codesign -v PyPixPro.dmg && echo "✅ DMG signature verified"
    echo "\n✨ Build complete!"
    echo "📦 Your signed app and DMG are in: $(pwd)"
    echo "\nNext steps:"
    echo "1. Test the app locally"
    echo "2. Create a GitHub release"
    echo "3. Upload PyPixPro.dmg to the release"
} || {
    echo "\n❌ Build failed!"
    exit 1
}