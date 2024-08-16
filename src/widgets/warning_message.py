from PySide6.QtWidgets import QMessageBox

class warningMessage(QMessageBox):
    def __init__(self, windowTitle: str, text: str):
        super().__init__()
        self.setWindowTitle(windowTitle)
        self.setText(text)
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)