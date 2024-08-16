from PySide6.QtWidgets import  QDialog, QVBoxLayout, QPushButton

from widgets.point_dialog import PointDialog 
from widgets.warning_message import warningMessage

from geometria.reta import Reta

class LineDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inserir Reta")

        layout = QVBoxLayout()

        self.insert_point_a_button = QPushButton()
        self.insert_point_a_button.setText("Inserir Ponto A")
        self.insert_point_a_button.clicked.connect(lambda: self.open_point_dialog("A"))
        layout.addWidget(self.insert_point_a_button)

        self.insert_point_b_button = QPushButton("Inserir Ponto B")
        self.insert_point_b_button.clicked.connect(lambda: self.open_point_dialog("B"))
        layout.addWidget(self.insert_point_b_button)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def open_point_dialog(self, point_id: str):
        dialog = PointDialog()
        if dialog.exec() == QDialog.Accepted:
            try:
                point = dialog.get_values()
                if point_id == "A":
                    self.point_a = point
                    self.insert_point_a_button.setText("Alterar Ponto A")
                elif point_id == "B":
                    self.point_b = point
                    self.insert_point_b_button.setText("Alterar Ponto B")
                else:
                    raise ValueError("Identificador de ponto inválido")
            except ValueError as e:
                warning = warningMessage("Erro", str(e))
                warning.exec()
                self.reject()

    
    def get_line(self) -> Reta:
        if hasattr(self, 'point_a') and hasattr(self, 'point_b'):
            return Reta(self.point_a, self.point_b)
        else:
            warning = warningMessage("Erro", "Pontos A e B devem ser inseridos")
            warning.exec()
            raise ValueError("Pontos A e B devem ser inseridos")