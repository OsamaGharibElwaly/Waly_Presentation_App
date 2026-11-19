"""Off-thread export worker with progress reporting and cancellation."""
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

from backend.pipeline.orchestrator import Orchestrator


class ExportWorker(QThread):
    progress = pyqtSignal(int, str)
    failed = pyqtSignal(str)
    succeeded = pyqtSignal(str)

    def __init__(self, theme: dict, palette: dict, meta: dict, markdown: str, target: Path) -> None:
        super().__init__()
        self.payload = (theme, palette, meta, markdown, Path(target))

    def cancel(self) -> None:
        self.requestInterruption()

    def run(self) -> None:
        try:
            theme, palette, meta, markdown, target = self.payload
            if self.isInterruptionRequested():
                return
            report = lambda value, message: self._report(value, message)
            Orchestrator(theme=theme, palette=palette, meta=meta).run(markdown, target, report)
            if not self.isInterruptionRequested():
                self.succeeded.emit(str(target.resolve()))
        except Exception as exc:
            self.failed.emit(str(exc))

    def _report(self, value: int, message: str) -> None:
        if not self.isInterruptionRequested():
            self.progress.emit(value, message)
