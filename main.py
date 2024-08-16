from abc import ABC
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import QStyle, QGridLayout, QVBoxLayout, QWidget,QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem, QMainWindow, QPushButton, QDockWidget
import xml.etree.ElementTree as ElementTree
import sys

class Ponto:
    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def print(self) -> None:
        print("x: " + str(self._x), "y: " + str(self._y), sep=", ")

class Retangulo(ABC):
    def __init__(self, p_minimo: Ponto, p_maximo: Ponto) -> None:
        if not all(isinstance(p, Ponto) for p in (p_minimo, p_maximo)):
            raise TypeError("As coordenadas devem ser um Ponto")
        self._p_minimo = p_minimo
        self._p_maximo = p_maximo

    @property
    def p_minimo(self) -> Ponto:
        return self._p_minimo

    @property
    def p_maximo(self) -> Ponto:
        return self._p_maximo

    def comprimento(self) -> float:
        return self._p_maximo.x - self._p_minimo.x

    def altura(self) -> float:
        return self._p_maximo.y - self._p_minimo.y

    def print(self) -> None:
        print("Ponto mínimo:", end=" ")
        self._p_minimo.print()
        print("Ponto máximo:", end=" ")
        self._p_maximo.print()
        print("Dimensão:", end=" ")
        print(self.comprimento(), self.altura(), sep="x")

class Window(Retangulo):
    def print(self) -> None:
        print("---- Window ----")
        super().print()

class Viewport(Retangulo):
    def print(self) -> None:
        print("---- Viewport ----")
        super().print()

class Reta:
    def __init__(self, a: Ponto, b: Ponto) -> None:
        if not all(isinstance(p, Ponto) for p in (a, b)):
            raise TypeError("As coordenadas devem ser um Ponto")
        if a == b:
            raise ValueError("Pontos da reta não podem coincidir")
        self._a = a
        self._b = b

    @property
    def a(self) -> Ponto:
        return self._a

    @property
    def b(self) -> Ponto:
        return self._b

    def tamanho(self) -> float:
        dx = self._b.x - self._a.x
        dy = self._b.y - self._a.y
        return (dx**2 + dy**2)**0.5

    def print(self) -> None:
        print("---- Reta ----")
        self._a.print()
        self._b.print()
        print("Tamanho: ", self.tamanho())

class Poligono:
    def __init__(self, *pontos: Ponto) -> None:
        if not all(isinstance(p, Ponto) for p in pontos):
            raise TypeError("As coordenadas devem ser um Ponto")
        if len(pontos) <= 2:
            raise ValueError("Quantidade de pontos do poligono deve ser maior que 2")
        self._pontos = list(pontos)

    @property
    def pontos(self) -> list[Ponto]:
        return self._pontos

    def print(self) -> None:
        print("---- Poligono ----")
        for ponto in self._pontos:
            ponto.print()

class ViewportWindow(QWidget):
    def __init__(self, viewport, pontos, retas, poligonos):
        super().__init__()
        self.viewport = viewport
        self.pontos = pontos
        self.retas = retas
        self.poligonos = poligonos

        layout = QVBoxLayout()
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        layout.addWidget(self.view)
        self.setLayout(layout)

        self.update_scene()

    def update_scene(self):
        self.scene.clear()

        # Set the scene rect according to the viewport dimensions
        self.view.setSceneRect(
            self.viewport.p_minimo.x, 
            self.viewport.p_minimo.y, 
            self.viewport.comprimento(), 
            self.viewport.altura()
        )

        # Adicionar pontos
        for ponto in self.pontos:
            ponto_vp = QGraphicsEllipseItem(ponto.x, ponto.y, 1, 1)
            self.scene.addItem(ponto_vp)

        # Adicionar retas
        for reta in self.retas:
            reta_vp = QGraphicsLineItem(reta.a.x, reta.a.y, reta.b.x, reta.b.y)
            self.scene.addItem(reta_vp)

        # Adicionar polígonos
        for poligono in self.poligonos:
            poligono_vp = QGraphicsPolygonItem()
            poligono_vp.setPolygon(QPolygonF([QPointF(ponto.x, ponto.y) for ponto in poligono.pontos]))
            self.scene.addItem(poligono_vp)

    def move_left(self):
        # Move the viewport to the left by shifting the scene rect
        delta_x = 10  # Adjust the amount to move left by
        self.viewport.p_minimo.x -= delta_x
        self.viewport.p_maximo.x -= delta_x

        # Update the scene to reflect the changes
        self.update_scene()

    def move_right(self):
        delta_x = 10
        self.viewport.p_minimo.x += delta_x
        self.viewport.p_maximo.x += delta_x
        self.update_scene()

    def move_up(self):
        delta_y = 10
        self.viewport.p_minimo.y -= delta_y
        self.viewport.p_maximo.y -= delta_y
        self.update_scene()

    def move_down(self):
        delta_y = 10
        self.viewport.p_minimo.y += delta_y
        self.viewport.p_maximo.y += delta_y
        self.update_scene()

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
        insert_menu.addAction("Ponto")
        insert_menu.addAction("Reta")
        insert_menu.addAction("Poligono")
        export_menu = menu_bar.addMenu("Exportar")

        right_button.clicked.connect(self.viewport.move_right)
        left_button.clicked.connect(self.viewport.move_left)
        up_button.clicked.connect(self.viewport.move_up)
        down_button.clicked.connect(self.viewport.move_down)

def transformar_pontos_viewport(window: Window, viewport: Viewport, pontos: list[Ponto]) -> list[Ponto]:
    pontos_vp = []
    for ponto in pontos:
        x_vp = ((ponto.x - window.p_minimo.x) / window.comprimento()) * viewport.comprimento()
        y_vp = (1 - ((ponto.y - window.p_minimo.y) / window.altura())) * viewport.altura()
        pontos_vp.append(Ponto(x_vp, y_vp))
    return pontos_vp

if __name__ == "__main__":
    dados = ElementTree.parse('docs/entrada.xml').getroot()

    # ---- Window ----
    w_min = Ponto(*dados.find("window/wmin").attrib.values())
    w_max = Ponto(*dados.find("window/wmax").attrib.values())
    window = Window(w_min, w_max)
    window.print()

    # ---- Viewport ----
    vp_min = Ponto(*dados.find("viewport/vpmin").attrib.values())
    vp_max = Ponto(*dados.find("viewport/vpmax").attrib.values())
    viewport = Viewport(vp_min, vp_max)
    viewport.print()

    # ---- Pontos ----
    pontos = [Ponto(*ponto.attrib.values()) for ponto in dados.findall("ponto")]
    for ponto in pontos:
        ponto.print()

    # ---- Retas ----
    retas = [
        Reta(*(Ponto(*ponto.attrib.values()) for ponto in reta))
        for reta in dados.findall("reta")
    ]
    for reta in retas:
        reta.print()

    # ---- Polígonos ----
    poligonos = [
        Poligono(*(Ponto(*ponto.attrib.values()) for ponto in poligono))
        for poligono in dados.findall("poligono")
    ]
    for poligono in poligonos:
        poligono.print()

    # Limpa a estrutura antiga
    dados.clear()

    # ---- Transformar pontos para Viewport ----
    pontos = transformar_pontos_viewport(window, viewport, pontos)
    for ponto in pontos:
        ponto_elem = ElementTree.SubElement(dados, 'ponto')
        ponto_elem.set("x", str(ponto.x))
        ponto_elem.set("y", str(ponto.y))
        ponto.print()

    # ---- Transformar retas para viewport ----
    retas = [Reta(*transformar_pontos_viewport(window, viewport, [reta.a, reta.b])) for reta in retas]
    for reta in retas:
        reta_elem = ElementTree.SubElement(dados, "reta")
        for ponto in [reta.a, reta.b]:
            ponto_elem = ElementTree.SubElement(reta_elem, "ponto")
            ponto_elem.set("x", str(ponto.x))
            ponto_elem.set("y", str(ponto.x))
        reta.print()

    # ---- Transformar polígonos para viewport ----
    poligonos = [Poligono(*transformar_pontos_viewport(window, viewport, poligono.pontos)) for poligono in poligonos]
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

    # ---- Gerar Viewport ----
    app = QApplication(sys.argv)
    viewport_window = ViewportWindow(viewport, pontos, retas, poligonos)
    window = MainWindow(viewport_window)

    window.show()
    sys.exit(app.exec())
