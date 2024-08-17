from xml.etree import ElementTree
from widgets.point_dialog import PointDialog
from widgets.line_dialog import LineDialog
from widgets.poligono_dialog import PolygonDialog
from widgets.viewportwindow import ViewportWindow

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QStyle, QGridLayout, QWidget, QMainWindow, QPushButton, QDockWidget

class MainWindow(QMainWindow):
    def __init__(self, viewport: ViewportWindow):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.viewport = viewport

        dock_widget = QDockWidget("Controls", self)
        dock_widget.setMaximumHeight(300)

        dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        dock_contents = QWidget()
        dock_layout = QGridLayout()

        style = self.style()
        up_button = QPushButton()
        up_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        down_button = QPushButton()
        down_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        left_button = QPushButton()
        left_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
        right_button = QPushButton()
        right_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        rotate_left_button = QPushButton()
        rotate_right_button = QPushButton()
        rotate_left_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        rotate_right_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload))

        zoom_in_button = QPushButton("+")
        zoom_out_button = QPushButton("-")

        dock_layout.addWidget(up_button, 0, 1)
        dock_layout.addWidget(left_button, 1, 0)
        dock_layout.addWidget(right_button, 1, 2)
        dock_layout.addWidget(down_button, 2, 1)
        dock_layout.addWidget(rotate_left_button, 3, 0)
        dock_layout.addWidget(rotate_right_button, 3, 2)
        dock_layout.addWidget(zoom_in_button, 5, 0)
        dock_layout.addWidget(zoom_out_button, 5, 2)

        dock_contents.setLayout(dock_layout)
        dock_widget.setWidget(dock_contents)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

        self.setCentralWidget(self.viewport)

        menu_bar = self.menuBar()
        insert_menu = menu_bar.addMenu("Inserir")

        insert_point_action = insert_menu.addAction("Ponto")
        insert_line_action = insert_menu.addAction("Reta")
        insert_poligon_action = insert_menu.addAction("Poligono")

        export_menu_action = menu_bar.addMenu("Exportar").addAction("xml")
        export_menu_action.triggered.connect(self.export)

        insert_point_action.triggered.connect(self.open_point_dialog)
        insert_line_action.triggered.connect(self.open_line_dialog)
        insert_poligon_action.triggered.connect(self.open_poligono_dialog)

        #these next lines are used to implement a click and hold functionality to the movement buttons
        #the timer is used to make the viewport move
        self.right_timer = QTimer(self)
        self.left_timer = QTimer(self)
        self.up_timer = QTimer(self)
        self.down_timer = QTimer(self)

        #the interval is the time between each movement
        self.right_timer.setInterval(50)
        self.left_timer.setInterval(50)
        self.up_timer.setInterval(50)
        self.down_timer.setInterval(50)

        #the viewport is moved when the timer times out
        self.right_timer.timeout.connect(self.viewport.move_right)
        self.left_timer.timeout.connect(self.viewport.move_left)
        self.up_timer.timeout.connect(self.viewport.move_up)
        self.down_timer.timeout.connect(self.viewport.move_down)

        #the viewport stops moving when the button is released
        right_button.pressed.connect(self.right_timer.start)
        right_button.released.connect(self.right_timer.stop)

        left_button.pressed.connect(self.left_timer.start)
        left_button.released.connect(self.left_timer.stop)

        up_button.pressed.connect(self.up_timer.start)
        up_button.released.connect(self.up_timer.stop)

        down_button.pressed.connect(self.down_timer.start)
        down_button.released.connect(self.down_timer.stop)

        rotate_left_button.clicked.connect(lambda: self.viewport.rotate_objects(-10))
        rotate_right_button.clicked.connect(lambda: self.viewport.rotate_objects(10))

        zoom_in_button.clicked.connect(self.viewport.zoom_in)
        zoom_out_button.clicked.connect(self.viewport.zoom_out)

    def open_point_dialog(self):
        dialog = PointDialog()
        if dialog.exec() == QDialog.Accepted:
            point = dialog.get_values()
            self.viewport.pontos.append(point)
            self.viewport.update_scene()

    def open_line_dialog(self):
        dialog = LineDialog()
        if dialog.exec() == QDialog.Accepted:
            line = dialog.get_line()
            self.viewport.retas.append(line)
            self.viewport.update_scene()

    def open_poligono_dialog(self):
        dialog = PolygonDialog()
        if dialog.exec() == QDialog.Accepted:
            polygon = dialog.get_polygon()
            self.viewport.poligonos.append(polygon)
            self.viewport.update_scene()

    def export(self):
        dados = ElementTree.parse('docs/entrada.xml').getroot()
        dados.clear()

        pontos = self.viewport.pontos
        for ponto in pontos:
            ponto_elem = ElementTree.SubElement(dados, 'ponto')
            ponto_elem.set("x", str(ponto.x))
            ponto_elem.set("y", str(ponto.y))
            ponto.print()

        retas = self.viewport.retas
        for reta in retas:
            reta_elem = ElementTree.SubElement(dados, "reta")
            for ponto in [reta.a, reta.b]:
                ponto_elem = ElementTree.SubElement(reta_elem, "ponto")
                ponto_elem.set("x", str(ponto.x))
                ponto_elem.set("y", str(ponto.x))
            reta.print()

        # ---- Transformar polígonos para viewport ----
        poligonos = self.viewport.poligonos
        for poligono in poligonos:
            poligono_elem = ElementTree.SubElement(dados, "poligono")
            for ponto in poligono.pontos:
                ponto_elem = ElementTree.SubElement(poligono_elem, "ponto")
                ponto_elem.set("x", str(ponto.x))
                ponto_elem.set("y", str(ponto.x))
            poligono.print()

        # Salva o arquivo com a nova estrutura
        xml = ElementTree.ElementTree(dados)
        ElementTree.indent(xml, space="\t", level=0)
        xml.write("docs/saida.xml", xml_declaration=True, encoding="utf-8")