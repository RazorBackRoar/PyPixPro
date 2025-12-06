import logging
import sys
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QTextEdit,
    QInputDialog,
)
from PySide6.QtCore import Qt, QObject, Signal, QThread
from PySide6.QtGui import QPixmap, QIcon

from ..core.processor import run_processing
from ..utils import get_resource_path

logger = logging.getLogger(__name__)


class SignaledLogHandler(logging.Handler, QObject):
    log_signal = Signal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)


class WorkerThread(QThread):
    finished_signal = Signal()

    def __init__(self, folder_path, portrait_prefix, landscape_prefix):
        super().__init__()
        self.folder_path = folder_path
        self.portrait_prefix = portrait_prefix
        self.landscape_prefix = landscape_prefix

    def run(self):
        try:
            run_processing(
                self.folder_path, self.portrait_prefix, self.landscape_prefix
            )
        except Exception as e:
            logging.error(f"Critical error in processing: {e}")
        finally:
            self.finished_signal.emit()


class DragDropWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_processing = False
        self.failure_log_path = Path.home() / "Desktop" / "PyPixPro Failure Log.txt"

        # Window configuration
        self.setWindowTitle("PyPixPro")
        self.setFixedSize(400, 400)  # Smaller size
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Setup views
        self.setup_window_image()
        self.setup_summary_display()

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Setup logging to GUI
        self.log_handler = SignaledLogHandler()
        self.log_handler.setFormatter(logging.Formatter("%(message)s"))
        self.log_handler.log_signal.connect(self.append_log)

        # Add handler to root logger to capture all logs (including core)
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)

    def setup_window_image(self):
        try:
            self.image_widget = QLabel()

            # Determine resource path
            image_path = get_resource_path(
                os.path.join("assets", "images", "PyPixProBackground.png")
            )

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                # Scale to cover
                scaled_pixmap = pixmap.scaled(
                    400,
                    400,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Center Crop
                x = (scaled_pixmap.width() - 400) // 2
                y = (scaled_pixmap.height() - 400) // 2
                cropped_pixmap = scaled_pixmap.copy(x, y, 400, 400)

                self.image_widget.setPixmap(cropped_pixmap)
            else:
                logger.warning(f"Image not found at {image_path}")
                self.image_widget.setText("")
                self.image_widget.setStyleSheet("background-color: #333;")

            self.image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stacked_widget.addWidget(self.image_widget)

        except Exception as e:
            logger.error(f"Error loading window image: {e}")
            self.image_widget = QLabel("")
            self.stacked_widget.addWidget(self.image_widget)

    def setup_summary_display(self):
        self.summary_widget = QTextEdit()
        self.summary_widget.setReadOnly(True)
        self.summary_widget.setStyleSheet(
            """
            QTextEdit {
                background-color: black;
                color: white;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                padding: 20px;
                border: none;
            }
        """
        )
        self.stacked_widget.addWidget(self.summary_widget)

    def append_log(self, message):
        self.summary_widget.append(message)
        # Scroll to bottom
        scrollbar = self.summary_widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and not self.is_processing:
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime = event.mimeData()
        if not mime.hasUrls():
            return

        dropped_path = Path(mime.urls()[0].toLocalFile())
        if not dropped_path.exists() or not dropped_path.is_dir():
            QMessageBox.warning(self, "Error", "Please drop a valid folder.")
            return

        # Ask for prefixes
        portrait_prefix, ok1 = QInputDialog.getText(
            self, "Configuration", "Enter Portrait Prefix:", text="Portrait"
        )
        if not ok1:
            return

        landscape_prefix, ok2 = QInputDialog.getText(
            self, "Configuration", "Enter Landscape Prefix:", text="Landscape"
        )
        if not ok2:
            return

        # Switch to log view
        self.stacked_widget.setCurrentWidget(self.summary_widget)
        self.summary_widget.clear()
        self.is_processing = True
        self.setAcceptDrops(False)

        # Start processing in background thread
        self.worker = WorkerThread(dropped_path, portrait_prefix, landscape_prefix)
        self.worker.finished_signal.connect(self.on_processing_finished)
        self.worker.start()

    def on_processing_finished(self):
        self.is_processing = False
        self.setAcceptDrops(True)
        QMessageBox.information(self, "Complete", "Processing finished successfully!")
        # Optionally switch back to image or keep logs
        # self.stacked_widget.setCurrentWidget(self.image_widget)

    def closeEvent(self, event):
        # Clean up
        try:
            if hasattr(self, "worker") and self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
        except:
            pass
        event.accept()
