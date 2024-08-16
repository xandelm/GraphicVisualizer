from geometria.ponto import Ponto
from geometria.retangulo import Retangulo
from geometria.reta import Reta
from geometria.poligono import Poligono

from widgets.viewportwindow import ViewportWindow
from widgets.mainwindow import MainWindow

from PySide6.QtWidgets import QApplication

import xml.etree.ElementTree as ElementTree
import sys


class Window(Retangulo):
    def print(self) -> None:
        print("---- Window ----")
        super().print()

class Viewport(Retangulo):
    def print(self) -> None:
        print("---- Viewport ----")
        super().print()



""""TODO: Implementar a classe PoligonoDialog
class PoligonoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.windowTitle("Inserir Poligono")

        layout = QVBoxLayout()
        
"""
    
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
