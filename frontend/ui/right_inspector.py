"""Right-hand inspector: zone preview, motion simulation and guided export."""
from PyQt6.QtCore import QPropertyAnimation, QRectF, Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QToolBox, QVBoxLayout, QWidget,
)

from backend.layout.geometry import W, H, layout_zones


class ZonePreview(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(360, 230)
        self._placement = "split_right"
        self._progress = 0.0
        self._warning = ""
        self._step = 0
        self._timer = QTimer(self)
        self._timer.setInterval(750)
        self._timer.timeout.connect(self.step)
        self._motion = QPropertyAnimation(self, b"progress")
        self._motion.setDuration(1100)
        self._motion.setStartValue(0.0)
        self._motion.setEndValue(1.0)

    def get_progress(self) -> float:
        return self._progress

    def set_progress(self, value: float) -> None:
        self._progress = max(0.0, min(1.0, value))
        self.update()

    progress = pyqtProperty(float, get_progress, set_progress)

    def set_placement(self, placement: str, warning: str = "") -> None:
        self._placement = placement
        self._warning = warning
        self.update()

    def play(self) -> None:
        self._motion.stop()
        self._motion.start()
        self._timer.start()

    def replay(self) -> None:
        self._step = 0
        self.play()

    def step(self) -> None:
        self._step = (self._step + 1) % 4
        self._motion.stop()
        self.set_progress(self._step / 3)

    def stop(self) -> None:
        self._timer.stop()
        self._motion.stop()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0B1220"))
        scale = min(self.width() / W, self.height() / H) * 0.94
        offset_x = (self.width() - W * scale) / 2
        offset_y = (self.height() - H * scale) / 2
        slide = QRectF(offset_x, offset_y, W * scale, H * scale)
        painter.fillRect(slide, QColor("#111C33"))
        painter.setPen(QColor("#38BDF8"))
        painter.drawRect(slide)
        zones = layout_zones(self._placement)
        for name, box in zones.items():
            rect = QRectF(offset_x + box[0] * scale, offset_y + box[1] * scale,
                          box[2] * scale, box[3] * scale)
            color = QColor("#2563EB") if name == "image" else (
                QColor("#F59E0B") if name == "footer" else QColor("#10B981"))
            painter.fillRect(rect, QColor(color.red(), color.green(), color.blue(), 46))
            painter.setPen(color)
            painter.drawRect(rect)
            painter.drawText(rect.adjusted(4, 4, -4, -4), Qt.AlignmentFlag.AlignTop, name)
        content = zones["content"]
        travel = content[2] * scale * self._progress
        marker = QRectF(offset_x + content[0] * scale, offset_y + content[1] * scale,
                        max(6.0, travel), 8)
        painter.fillRect(marker, QColor("#F8FAFC"))
        painter.setPen(QColor("#F87171") if self._warning else QColor("#7DD3FC"))
        painter.drawText(6, self.height() - 6, self._warning or self._placement)
        painter.end()


class PreviewDialog(QDialog):
    def __init__(self, preview: ZonePreview, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Pop-Out Slide & Motion Preview")
        self.resize(1000, 620)
        layout = QVBoxLayout(self)
        self.preview = ZonePreview()
        self.preview.set_placement(preview._placement, preview._warning)
        self.preview.set_progress(preview.get_progress())
        layout.addWidget(self.preview, 1)
        close = QPushButton("Close")
        close.clicked.connect(self.close)
        layout.addWidget(close)


class RightInspectorPanel(QWidget):
    exportRequested = pyqtSignal(str)
    manifestRefreshRequested = pyqtSignal()

    def __init__(self, summary: str = "", manifest: list[dict] | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(320)
        self._summary = summary
        self._build_ui()
        self.set_manifest(manifest or [])
        self.set_summary(summary)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        self.tabs = QToolBox()
        root.addWidget(self.tabs, 1)

        preview_page = QWidget()
        preview_layout = QVBoxLayout(preview_page)
        self.preview = ZonePreview()
        preview_layout.addWidget(self.preview, 1)
        controls = QHBoxLayout()
        for label, handler in (("Play", self.preview.play), ("Replay", self.preview.replay),
                               ("Step", self.preview.step)):
            button = QPushButton(label)
            button.clicked.connect(handler)
            controls.addWidget(button)
        popout = QPushButton("Pop-Out Preview")
        popout.clicked.connect(self._pop_out)
        controls.addWidget(popout)
        preview_layout.addLayout(controls)
        self.summary_lbl = QLabel("")
        self.summary_lbl.setWordWrap(True)
        self.summary_lbl.setStyleSheet("color: #7DD3FC; padding: 6px;")
        preview_layout.addWidget(self.summary_lbl)
        self.tabs.addItem(preview_page, "Preview & Animation")

        guided = QWidget()
        guided_layout = QVBoxLayout(guided)
        self.safety_lbl = QLabel("Deck & text safety: waiting for Markdown")
        self.pool_lbl = QLabel("Visual pool: 0 assets")
        refresh = QPushButton("Refresh visual pool manifest")
        refresh.clicked.connect(lambda: self.manifestRefreshRequested.emit())
        motion = QLabel("Motion presets are applied to PowerPoint timing on export.")
        motion.setWordWrap(True)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PowerPoint (.pptx)", "PDF (.pdf)"])
        self.guided_export = QPushButton("Run guided export")
        self.guided_export.setStyleSheet("background-color: #047857; color: #FFFFFF;")
        self.guided_export.clicked.connect(self._request_export)
        self.guided_status = QLabel("Ready")
        self.guided_progress = QProgressBar()
        self.guided_progress.setRange(0, 100)
        steps = QToolBox()
        step_one = QWidget()
        one_layout = QVBoxLayout(step_one)
        one_layout.addWidget(self.safety_lbl)
        steps.addItem(step_one, "1. Deck & Text Safety")
        step_two = QWidget()
        two_layout = QVBoxLayout(step_two)
        two_layout.addWidget(self.pool_lbl)
        two_layout.addWidget(refresh)
        two_layout.addWidget(motion)
        steps.addItem(step_two, "2. Visual Pool & Motion")
        step_three = QWidget()
        three_layout = QVBoxLayout(step_three)
        three_layout.addWidget(self.format_combo)
        three_layout.addWidget(self.guided_export)
        three_layout.addWidget(self.guided_progress)
        three_layout.addWidget(self.guided_status)
        steps.addItem(step_three, "3. Export Target")
        guided_layout.addWidget(steps)
        self.tabs.addItem(guided, "Guided Settings")

    def _request_export(self) -> None:
        self.exportRequested.emit("pptx" if self.format_combo.currentIndex() == 0 else "pdf")

    def _pop_out(self) -> None:
        PreviewDialog(self.preview, self).exec()

    def set_preview(self, placement: str, warning: str = "") -> None:
        self.preview.set_placement(placement, warning)

    def set_summary(self, text: str) -> None:
        self.summary_lbl.setText(text or "No transition settings selected")

    def set_manifest(self, items: list[dict]) -> None:
        self.pool_lbl.setText(f"Visual pool: {len(items)} pre-built assets")

    def set_text_status(self, text: str) -> None:
        self.safety_lbl.setText(f"Deck & text safety: {text}")

    def set_progress(self, value: int, message: str = "") -> None:
        self.guided_progress.setValue(value)
        self.guided_status.setText(message or f"{value}%")
