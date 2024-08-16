from widgets.point_dialog import PointDialog
from widgets.line_dialog import LineDialog
from widgets.viewportwindow import ViewportWindow

from PySide6.QtCore import Qt
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
        
        export_menu = menu_bar.addMenu("Exportar")

        insert_point_action.triggered.connect(self.open_point_dialog)
        insert_line_action.triggered.connect(self.open_line_dialog)
        #TODO: Implementar método para abrir o diálogo de polígonos
        #insert_poligon_action.triggered.connect(self.open_poligono_dialog)

        right_button.clicked.connect(self.viewport.move_right)
        left_button.clicked.connect(self.viewport.move_left)
        up_button.clicked.connect(self.viewport.move_up)
        down_button.clicked.connect(self.viewport.move_down)
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

    #TODO: Implementar método para abrir o diálogo de polígonos
    #def open_poligono_dialog(self):