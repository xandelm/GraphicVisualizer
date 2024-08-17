from PySide6.QtWidgets import  QDialog, QGridLayout, QPushButton

from widgets.point_dialog import PointDialog
from widgets.warning_message import warningMessage

from geometria.poligono import Poligono

class PolygonDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inserir Polígono")
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.points = []
        self.layoutGrid = QGridLayout()

        self.point_count = 0

        self.plus_button = QPushButton("+");
        self.plus_button.clicked.connect(self.add_new_point_button)
        self.layoutGrid.addWidget(self.plus_button, 1, 0)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layoutGrid.addWidget(self.ok_button, 1, 1)

        self.setLayout(self.layoutGrid)

    def add_new_point_button(self):
        if (self.point_count > len(self.alphabet)):
            warning = warningMessage("Não é possível mais adicinar pontos")
            warning.exec()
        self.insert_new_point_button = QPushButton("Inserir Ponto " + self.alphabet[self.point_count]);
        self.insert_new_point_button.clicked.connect(lambda: self.open_point_dialog())
        self.layoutGrid.addWidget(self.insert_new_point_button, 0, self.point_count)
        self.point_count += 1

    def open_point_dialog(self):
        dialog = PointDialog()
        if dialog.exec() == QDialog.Accepted:
            try:
                point = dialog.get_values()
                list.append(self.points, point)
            except ValueError as e:
                warning = warningMessage("Erro", str(e))
                warning.exec()
                self.reject()

    def get_polygon(self) -> Poligono:
        lastPoint = self.points[0]
        list.append(self.points, lastPoint)
        return Poligono(*self.points)
