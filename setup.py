from pathlib import Path

from setuptools import find_packages, setup

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


def get_project_version(default: str = "0.0.0") -> str:
    pyproject = Path(__file__).resolve().parent / "pyproject.toml"
    if not pyproject.exists():
        return default
    try:
        with pyproject.open("rb") as fp:
            data = tomllib.load(fp)
        return data["project"]["version"]
    except Exception:
        return default


# --- Application Configuration (Single Source of Truth) ---
APP_NAME = "PyPixPro"
APP_SCRIPT = "src/pypixpro/main.py"
APP_VERSION = get_project_version()
BUNDLE_ID = "com.razorbackroar.pypixpro.app"
AUTHOR_NAME = "RazorBackRoar"

# --- Resource Files ---
DATA_FILES = [("", ["LICENSE"])]

# --- Info.plist Configuration ---
PLIST = {
    "CFBundleName": APP_NAME,
    "CFBundleDisplayName": APP_NAME,
    "CFBundleVersion": APP_VERSION,
    "CFBundleShortVersionString": APP_VERSION,
    "CFBundleIdentifier": BUNDLE_ID,
    "LSMinimumSystemVersion": "11.0",
    "NSHumanReadableCopyright": f"Copyright © 2025 {AUTHOR_NAME}. All rights reserved.",
    "NSPhotoLibraryUsageDescription": "PyPixPro needs access to your Photos library to organize and process images.",
    "LSRequiresNativeExecution": True,
    "LSApplicationCategoryType": "public.app-category.photography",
}

# --- py2app Options ---
OPTIONS = {
    "iconfile": "assets/icons/pypixpro.icns",
    "packages": ["PySide6"],
    "plist": PLIST,
    "bdist_base": "build/temp",
    "dist_dir": "build/dist",
    "strip": True,
    "argv_emulation": False,
    "includes": [
        "shiboken6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
    ],
    "excludes": [
        "tkinter",
        "PyInstaller",
        "numpy",
        "pandas",
        "IPython",
        "jupyter_client",
        "ipykernel",
        "tornado",
        "zmq",
        "botocore",
        "test",
        "unittest",
        "PySide6.QtWebEngine",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.Qt3DCore",
        "PySide6.Qt3DRender",
        "PySide6.Qt3DInput",
        "PySide6.Qt3DAnimation",
        "PySide6.Qt3DExtras",
        "PySide6.QtCharts",
        "PySide6.QtDataVisualization",
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
        "PySide6.QtQuick",
        "PySide6.QtQuick3D",
        "PySide6.QtQuickControls2",
        "PySide6.QtQuickWidgets",
        "PySide6.QtPdf",
        "PySide6.QtPdfWidgets",
        "PySide6.QtQml",
        "PySide6.QtSensors",
        "PySide6.QtSerialPort",
        "PySide6.QtSql",
        "PySide6.QtTest",
        "PySide6.QtBluetooth",
        "PySide6.QtLocation",
        "PySide6.QtPositioning",
        "PySide6.QtRemoteObjects",
        "PySide6.QtScxml",
        "PySide6.QtVirtualKeyboard",
        "PySide6.QtWebChannel",
        "PySide6.QtWebSockets",
    ],
}

# --- Setup Definition ---
setup(
    app=[APP_SCRIPT],
    name=APP_NAME,
    author=AUTHOR_NAME,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
