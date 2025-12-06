import logging
import os
import re
import shutil
from pathlib import Path
import blake3
from PIL import Image
import pillow_heif

# Register HEIF opener to handle HEIC files
pillow_heif.register_heif_opener()

# Configure logging for this module
logger = logging.getLogger(__name__)

# --- Constants ---
PORTRAIT_FOLDER_NAME = "Portrait"
LANDSCAPE_FOLDER_NAME = "Landscape"
GIF_FOLDER_NAME = "GIF"
RANDOM_FOLDER_NAME = "Random"
PRORAW_FOLDER_NAME = "ProRaw"
SCREENSHOTS_FOLDER_NAME = "Screenshots"

EXCLUDE_FILES = {".ds_store", "thumbs.db", "desktop.ini"}

# --- Core Logic Functions ---


def backup_folder(src_folder):
    """Create a backup of the input folder on the Desktop."""
    backup_path = Path.home() / "Desktop" / f"{src_folder.name}_Backup"
    try:
        if not backup_path.exists():
            shutil.copytree(src_folder, backup_path, dirs_exist_ok=True)
            logger.info(f"✅ Backup completed at: {backup_path}")
        else:
            logger.info(f"✅ Backup already exists at: {backup_path}")
    except Exception as e:
        logger.error(f"❌ Backup failed: {e}")


def generate_checksums(root_folder):
    """Generate a dictionary of checksums for all files in the root folder."""
    checksums = {}
    for path in root_folder.rglob("*"):
        if path.is_file() and not is_excluded(path):
            try:
                with open(path, "rb") as f:
                    file_hash = blake3.blake3(f.read()).hexdigest()
                checksums.setdefault(file_hash, []).append(path)
            except Exception as e:
                logger.error(f"❌ Error generating checksum for {path}: {e}")
    return checksums


def is_excluded(path):
    """Check if a file should be excluded."""
    name_lower = path.name.lower()
    return name_lower in EXCLUDE_FILES or name_lower.startswith("icon")


def delete_duplicates(root_folder):
    """Delete duplicate files based on checksums."""
    checksums = generate_checksums(root_folder)
    deleted_count = {}  # Track deleted counts per extension
    for file_list in checksums.values():
        if len(file_list) > 1:
            # Keep the first file, delete the rest
            for duplicate in file_list[1:]:
                try:
                    ext = duplicate.suffix.lower()
                    deleted_count[ext] = deleted_count.get(ext, 0) + 1
                    duplicate.unlink()
                    logger.info(f"✅ Deleted duplicate: {duplicate}")
                except Exception as e:
                    logger.error(f"❌ Error deleting duplicate {duplicate}: {e}")
    return deleted_count


def rename_files(target_folder, prefix):
    """Rename files sequentially with the given prefix and orientation."""
    if target_folder.name in [RANDOM_FOLDER_NAME, SCREENSHOTS_FOLDER_NAME]:
        logger.info(f"⏩ Skipping renaming for folder: {target_folder.name}")
        return  # Exit the function without renaming files in Random or Screenshots

    files = sorted(target_folder.glob("*"))
    for idx, file in enumerate(files, 1):
        # Skip renaming for non-image file types:
        if file.suffix.lower() not in (
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tiff",
            ".tif",
            ".psd",
            ".svg",
            ".ico",
            ".jfif",
            ".pjpeg",
            ".pjp",
            ".avif",
            ".apng",
            ".heic",
            ".heif",
        ):
            continue  # Skip to the next file

        # Determine the orientation (V or W) based on the target folder name
        orientation = "V" if target_folder.name == PORTRAIT_FOLDER_NAME else "W"

        # Use the user-provided prefix if it exists; otherwise, default to folder name
        effective_prefix = prefix if prefix else target_folder.name

        # Construct the new file name with correct spacing
        new_name = f"{effective_prefix} {orientation} {str(idx).zfill(3)}{file.suffix}"

        try:
            file.rename(target_folder / new_name)
            logger.info(f"✅ Renamed: '{file.name}' to '{new_name}'")
        except Exception as e:
            logger.error(f"❌ Error renaming {file.name}: {e}")


def process_heic_image(path):
    """Process HEIC image to determine its dimensions."""
    try:
        heif_file = pillow_heif.read_heif(path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        width, height = image.size
        logger.info(f"✅ Processed HEIC: {path.name} - {width}x{height}")
        return width, height
    except Exception as e:
        logger.error(f"❌ Error processing HEIC {path}: {e}")
        return None, None


def sort_files(root_folder, portrait_prefix, landscape_prefix):
    """Sort files into appropriate folders based on type and aspect ratio."""
    counts = {"Portrait": 0, "Landscape": 0, "Total Files": 0}
    dynamic_folders = {}

    for path in root_folder.rglob("*"):
        if path.is_file() and not is_excluded(path):
            counts["Total Files"] += 1
            suffix = path.suffix.lower()

            try:
                if suffix in (".heic", ".heif"):
                    width, height = process_heic_image(path)
                    if width and height:
                        if height > width:
                            target_folder_name = PORTRAIT_FOLDER_NAME
                            counts["Portrait"] += 1
                        else:
                            target_folder_name = LANDSCAPE_FOLDER_NAME
                            counts["Landscape"] += 1
                        folder = dynamic_folders.setdefault(
                            target_folder_name, root_folder / target_folder_name
                        )
                        if not folder.exists():
                            folder.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(path), folder / path.name)
                        logger.info(
                            f"✅ Moved HEIC to {target_folder_name}: {path.name}"
                        )

                elif suffix in (
                    ".jpg",
                    ".jpeg",
                    ".bmp",
                    ".tiff",
                    ".tif",
                    ".psd",
                    ".svg",
                    ".ico",
                    ".jfif",
                    ".pjpeg",
                    ".pjp",
                    ".avif",
                    ".apng",
                ):
                    with Image.open(path) as img:
                        width, height = img.size
                        logger.info(
                            f"✅ Processed Image: {path.name} - {width}x{height}"
                        )
                        if height > width:
                            target_folder_name = PORTRAIT_FOLDER_NAME
                            counts["Portrait"] += 1
                        else:
                            target_folder_name = LANDSCAPE_FOLDER_NAME
                            counts["Landscape"] += 1
                        folder = dynamic_folders.setdefault(
                            target_folder_name, root_folder / target_folder_name
                        )
                        if not folder.exists():
                            folder.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(path), folder / path.name)
                        logger.info(
                            f"✅ Moved Image to {target_folder_name}: {path.name}"
                        )

                elif suffix == ".png":
                    folder = dynamic_folders.setdefault(
                        SCREENSHOTS_FOLDER_NAME, root_folder / SCREENSHOTS_FOLDER_NAME
                    )
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), folder / path.name)
                    logger.info(f"✅ Moved PNG (Screenshot): {path} to {folder}")

                elif suffix in (".gif", ".webp"):
                    folder = dynamic_folders.setdefault(
                        GIF_FOLDER_NAME, root_folder / GIF_FOLDER_NAME
                    )
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), folder / path.name)
                    logger.info(f"✅ Moved GIF: {path} to {folder}")

                elif suffix in (
                    ".dng",
                    ".raw",
                    ".nef",
                    ".cr2",
                    ".cr3",
                    ".arw",
                    ".orf",
                    ".rw2",
                    ".raf",
                    ".srw",
                    ".kdc",
                ):
                    folder = dynamic_folders.setdefault(
                        PRORAW_FOLDER_NAME, root_folder / PRORAW_FOLDER_NAME
                    )
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), folder / path.name)
                    logger.info(f"✅ Moved ProRaw: {path} to {folder}")

                else:
                    folder = dynamic_folders.setdefault(
                        RANDOM_FOLDER_NAME, root_folder / RANDOM_FOLDER_NAME
                    )
                    if not folder.exists():
                        folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), folder / path.name)
                    logger.info(f"✅ Moved Misc: {path} to {folder}")

            except Exception as e:
                logger.error(f"❌ Error processing {path}: {e}")

    return counts


def clean_filenames(root_folder):
    """Clean filenames by removing spaces and special characters."""
    renamed_files = []
    for path in root_folder.rglob("*"):
        if path.is_file() and not is_excluded(path):
            original_name = path.name
            # Keep spaces in filenames during cleaning
            cleaned_name = re.sub(r"[^\w\s\-\.]", "", original_name)
            cleaned_name = re.sub(
                r"\s+", " ", cleaned_name
            ).strip()  # Replace multiple spaces with single

            if cleaned_name and cleaned_name != original_name:
                new_path = path.parent / cleaned_name
                try:
                    path.rename(new_path)
                    renamed_files.append((original_name, cleaned_name))
                except Exception as e:
                    logger.error(f"❌ Failed to rename '{original_name}': {e}")

    if renamed_files:
        logger.info("\n✅ Renaming Operations:")
        for original, cleaned in renamed_files:
            logger.info(f"Renamed: '{original}' to '{cleaned}'")
    else:
        logger.info("\n✅ No filenames needed renaming.")

    logger.info(
        f"\n✅ Filename cleaning complete. Total files renamed: {len(renamed_files)}"
    )


def count_files(root_folder):
    """Count initial files per extension."""
    initial_count = {}
    for path in root_folder.rglob("*"):
        if path.is_file() and not is_excluded(path):
            ext = path.suffix.lower()
            initial_count[ext] = initial_count.get(ext, 0) + 1
    return initial_count


def count_remaining_files(root_folder):
    """Count remaining files per extension after deletion."""
    remaining_count = {}
    for path in root_folder.rglob("*"):
        if path.is_file() and not is_excluded(path):
            ext = path.suffix.lower()
            remaining_count[ext] = remaining_count.get(ext, 0) + 1
    return remaining_count


def print_summary_table(initial_count, deleted_count, remaining_count):
    """Print a summary table of file counts."""
    total_pre = sum(initial_count.values())
    total_dups = sum(deleted_count.values())
    total_post = sum(remaining_count.values())

    # ANSI escape codes for table borders
    TOP_LEFT = "\033[34m╔\033[0m"
    TOP_RIGHT = "\033[34m╗\033[0m"
    BOTTOM_LEFT = "\033[34m╚\033[0m"
    BOTTOM_RIGHT = "\033[34m╝\033[0m"
    HORIZONTAL = "\033[34m═\033[0m"
    VERTICAL = "\033[34m║\033[0m"
    T_DOWN = "\033[34m╦\033[0m"
    T_UP = "\033[34m╩\033[0m"
    T_LEFT = "\033[34m╣\033[0m"
    T_RIGHT = "\033[34m╠\033[0m"
    CROSS = "\033[34m╬\033[0m"

    # Print the table header
    logger.info("\n")
    logger.info(
        f"{TOP_LEFT}{HORIZONTAL*12}{T_DOWN}{HORIZONTAL*12}{T_DOWN}{HORIZONTAL*12}{T_DOWN}{HORIZONTAL*12}{TOP_RIGHT}"
    )
    logger.info(
        f"{VERTICAL} {'Extension':<10} {VERTICAL} {'PreCount':<10} {VERTICAL} {'Duplicates':<10} {VERTICAL} {'PostCount':<10} {VERTICAL}"
    )
    logger.info(
        f"{T_RIGHT}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{T_LEFT}"
    )

    # Print each extension row
    for ext in sorted(initial_count.keys()):
        pre_count = initial_count.get(ext, 0)
        dups = deleted_count.get(ext, 0)
        post_count = remaining_count.get(ext, 0)
        logger.info(
            f"{VERTICAL} {ext:<10} {VERTICAL} {pre_count:<10} {VERTICAL} {dups:<10} {VERTICAL} {post_count:<10} {VERTICAL}"
        )

    # Print the totals
    logger.info(
        f"{T_RIGHT}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{CROSS}{HORIZONTAL*12}{T_LEFT}"
    )
    logger.info(
        f"{VERTICAL} {'Totals:':<10} {VERTICAL} {total_pre:<10} {VERTICAL} {total_dups:<10} {VERTICAL} {total_post:<10} {VERTICAL}"
    )
    logger.info(
        f"{BOTTOM_LEFT}{HORIZONTAL*12}{T_UP}{HORIZONTAL*12}{T_UP}{HORIZONTAL*12}{T_UP}{HORIZONTAL*12}{BOTTOM_RIGHT}"
    )
    logger.info("\n")


def run_processing(
    input_folder_path, portrait_prefix="Portrait", landscape_prefix="Landscape"
):
    """
    Run the photo processing workflow on the given folder.
    """
    root_folder = Path(input_folder_path).resolve()
    logger.info(f"📂 Processing folder: {root_folder}")

    if not root_folder.is_dir():
        logger.error(f"❌ Error: The path '{root_folder}' is not a valid directory.")
        return

    # Backup
    backup_folder(root_folder)

    # Count initial files
    logger.info("📊 Counting initial files...")
    initial_count = count_files(root_folder)

    # Duplicate Deletion
    logger.info("🔍 Deleting duplicates...")
    deleted_count = delete_duplicates(root_folder)

    # Count remaining files after deletion
    logger.info("📊 Counting remaining files...")
    remaining_count = count_remaining_files(root_folder)

    # Sorting
    logger.info("📂 Sorting files...")
    sort_counts = sort_files(root_folder, portrait_prefix, landscape_prefix)

    # Rename files in Portrait and Landscape folders
    logger.info("✍️ Renaming files in Portrait and Landscape folders...")
    for folder_name in [PORTRAIT_FOLDER_NAME, LANDSCAPE_FOLDER_NAME]:
        target_folder = root_folder / folder_name
        if target_folder.exists() and target_folder.is_dir():
            prefix = (
                portrait_prefix
                if folder_name == PORTRAIT_FOLDER_NAME
                else landscape_prefix
            )
            rename_files(target_folder, prefix)

    # Filename Cleaning
    logger.info("🧽 Cleaning filenames...")
    clean_filenames(root_folder)

    # Print Summary Table
    logger.info("📊 Summary Table:")
    print_summary_table(initial_count, deleted_count, remaining_count)

    logger.info("\n✅ Processing complete!")
