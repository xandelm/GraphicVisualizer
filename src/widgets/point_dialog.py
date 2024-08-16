from PySide6.QtWidgets import QLabel, QLineEdit, QDialog, QVBoxLayout ,QPushButton

from geometria.ponto import Ponto

from widgets.warning_message import warningMessage

class PointDialog(QDialog):
    def __init__(self, x_value: float = '' , y_value: float = ''):
        super().__init__()
        self.setWindowTitle("Inserir Ponto")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Insira o valor X:"))
        self.x_input = QLineEdit()
        self.x_input.setText(str(x_value))
        layout.addWidget(self.x_input)

        layout.addWidget(QLabel("Insira o valor Y:"))
        self.y_input = QLineEdit()
        self.y_input.setText(str(y_value))
        layout.addWidget(self.y_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_values(self) -> Ponto:
        x_text = self.x_input.text()
        y_text = self.y_input.text()
        if not x_text or not y_text:
            warning = warningMessage("Erro", "Os campos de entrada não podem estar vazios")
            warning.exec()
            raise ValueError("Os campos de entrada não podem estar vazios")
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
        except:
            warning = warningMessage("Erro", "Os valores inseridos devem ser numéricos")
            warning.exec()
            raise ValueError("Os valores inseridos devem ser numéricos")
        return Ponto(x, y)