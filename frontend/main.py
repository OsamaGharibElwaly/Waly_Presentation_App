"""Entry point for the PyQt6 desktop app."""
import sys
from pathlib import Path

# Automatically add the project root directory to sys.path so 'backend' and 'theme_factory' are found
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PyQt6.QtWidgets import QApplication
from frontend.ui.main_window import MainWindow  # Note the absolute package import


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Offline AI Presentation Factory")
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())