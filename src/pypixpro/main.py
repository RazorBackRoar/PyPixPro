#!/usr/bin/env python3

import logging
import os
import sys
from pathlib import Path

# Add src to path if running directly to allow absolute imports
if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

# Third-party imports
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Local imports
from pypixpro.core.processor import run_processing
from pypixpro.gui.main_window import DragDropWindow
from pypixpro.utils import get_resource_path

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- CLI Helper Functions ---


def usage():
    """Print usage instructions and exit."""
    logger.info("Usage: python3 -m pypixpro.main [folder_path]")
    sys.exit(1)


def get_input_folder():
    """Get and validate the input folder from command-line arguments or user input."""
    if len(sys.argv) > 1:
        # If arguments are passed, assume it's a path
        # Handle case where sys.argv[0] is the script name
        input_str = " ".join(sys.argv[1:]).strip()
        # Basic cleanup if needed, though shell usually handles quotes
        input_str = input_str.replace("\\ ", " ").strip('"').strip("'")
        input_folder = Path(input_str).resolve()

        if not input_folder.exists():
            # Fallback for potential drag-and-drop argument issues
            logger.warning(f"⚠️  Warning: Provided path '{input_str}' does not exist.")
            return None
    else:
        # If no args, return None to signal GUI mode
        return None

    forbidden_dirs = [Path("/System"), Path("/Library"), Path("/Applications")]
    for forbidden in forbidden_dirs:
        if forbidden == input_folder or forbidden in input_folder.parents:
            logger.error(
                f"❌ Error: The path '{input_folder}' is a protected system directory."
            )
            return None

    if not input_folder.is_dir():
        logger.error(f"❌ Error: The path '{input_folder}' is not a valid directory.")
        sys.exit(1)

    return input_folder


# --- Main Entry Point ---


def main():
    # Check if args provided for CLI usage
    input_folder = get_input_folder()

    if input_folder:
        # CLI Mode
        logger.info("🚀 Starting PyPixPro in CLI mode...")

        # Ask for Portrait and Landscape prefixes (CLI interactive)
        print("Enter a prefix for Portrait photos (or press Enter to use 'Portrait'):")
        portrait_prefix = input("> ").strip() or "Portrait"

        print(
            "Enter a prefix for Landscape photos (or press Enter to use 'Landscape'):"
        )
        landscape_prefix = input("> ").strip() or "Landscape"

        run_processing(input_folder, portrait_prefix, landscape_prefix)

    else:
        # GUI Mode
        # Only start GUI if no valid folder arg passed (or explicit launch)
        logger.info("🚀 Starting PyPixPro GUI...")
        app = QApplication(sys.argv)

        # Set App Icon
        app_icon_path = get_resource_path(
            os.path.join("assets", "icons", "pypixpro.icns")
        )
        if os.path.exists(app_icon_path):
            app.setWindowIcon(QIcon(app_icon_path))

        window = DragDropWindow()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
