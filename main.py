from abc import ABC
import random
from PySide6 import QtCore, QtWidgets, QtGui
import xml.etree.ElementTree as ElementTree

class Ponto:
    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

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
        self._pontos = list(pontos)

    @property
    def pontos(self) -> list[Ponto]:
        return self._pontos

    def print(self) -> None:
        print("---- Poligono ----")
        for ponto in self._pontos:
            ponto.print();

class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


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

    # ---- Poligonos ----
    poligonos = [
        Poligono(*(Ponto(*ponto.attrib.values()) for ponto in poligono))
        for poligono in dados.findall("poligono")
    ]
    for poligono in poligonos:
        poligono.print();

    # app = QtWidgets.QApplication([])

        # widget = MyWidget()
        # widget.resize(800, 600)
        # widget.show()
