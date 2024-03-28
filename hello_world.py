import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import xml.etree.ElementTree as ElementTree


class Ponto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def print(self):
        print("x: " + str(self.x), ", y: " + str(self.y))


class Coordenadas:
    def __init__(self, minimo: Ponto, maximo: Ponto):
        self.minimo = minimo
        self.maximo = maximo

    def print(self):
        print("minimo: ")
        self.minimo.print()
        print("maximo: ")
        self.maximo.print()


class Reta:
    def __init__(self, a: Ponto, b: Ponto):
        self.a = a
        self.b = b

    def print(self):
        self.a.print()
        self.b.print()


class Poligono:

    def __init__(self, *pontos: Ponto):
        self.pontos = list(pontos)


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
    # app = QtWidgets.QApplication([])

    # widget = MyWidget()
    # widget.resize(800, 600)
    # widget.show()

    # root = entrada.getroot()
    # print(root.tag, root.attrib)
    #    for child in root:
    #        print(child.tag, child.attrib)
    entrada = ElementTree.parse('docs/entrada.xml')
    root = entrada.getroot()
    vp_min = Ponto(*root.find("./viewport/vpmin").attrib.values())
    vp_max = Ponto(*root.find("./viewport/vpmax").attrib.values())
    viewport = Coordenadas(vp_min, vp_max)
    wmin = Ponto(*root.find("./window/wmin").attrib.values())
    wmax = Ponto(*root.find("./window/wmax").attrib.values())
    window = Coordenadas(wmin, wmax)
    window.print()
    viewport.print()
    pontos = [Ponto(*ponto.attrib.values()) for ponto in root.findall("./ponto")]
    for ponto in pontos:
        ponto.print()

    retas = [Reta(Ponto(*ponto.attrib.values()), Ponto(*ponto.attrib.values())) for reta in root.findall("./reta") for
             ponto
             in reta]
    print("Retas:")
    for reta in retas:
        reta.print()

    # sys.exit(app.exec())
