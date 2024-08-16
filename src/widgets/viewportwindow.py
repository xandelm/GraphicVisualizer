from geometria.ponto import Ponto

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem

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

        self.original_viewport_size = (viewport.comprimento(), viewport.altura())
        self.scale_factor = 1.0

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
        self.viewport.p_minimo.x += delta_x
        self.viewport.p_maximo.x += delta_x

        # Update the scene to reflect the changes
        self.update_scene()

    def move_right(self):
        delta_x = 10
        self.viewport.p_minimo.x -= delta_x
        self.viewport.p_maximo.x -= delta_x
        self.update_scene()

    def move_up(self):
        delta_y = 10
        self.viewport.p_minimo.y += delta_y
        self.viewport.p_maximo.y += delta_y
        self.update_scene()

    def move_down(self):
        delta_y = 10
        self.viewport.p_minimo.y -= delta_y
        self.viewport.p_maximo.y -= delta_y
        self.update_scene()
        
    def rotate_objects(self, angle):
        center = Ponto(
            (self.viewport.p_minimo.x + self.viewport.p_maximo.x) / 2,
            (self.viewport.p_minimo.y + self.viewport.p_maximo.y) / 2,
        )
        

        # Rotate all points
        for ponto in self.pontos:
            ponto.rotate(angle, center)

        # Rotate all lines
        for reta in self.retas:
            reta.a.rotate(angle, center)
            reta.b.rotate(angle, center)

        # Rotate all polygons
        for poligono in self.poligonos:
            for ponto in poligono.pontos:
                ponto.rotate(angle, center)

        # Update the scene with the new coordinates
        self.update_scene()

    def zoom_in(self):
        self.zoom(1.1)  # Ampliar em 10%

    def zoom_out(self):
        self.zoom(0.9)  # Reduzir em 10%

    def zoom(self, factor: float):
        # Atualiza o fator de escala
        self.scale_factor *= factor
        center = Ponto(
            (self.viewport.p_minimo.x + self.viewport.p_maximo.x) / 2,
            (self.viewport.p_minimo.y + self.viewport.p_maximo.y) / 2)
        
        for ponto in self.pontos:
            ponto.zoom(factor, center)

        self.apply_zoom(factor)

    def apply_zoom(self, factor: float):
                # Calcular o centro atual
        center_x = (self.viewport.p_minimo.x + self.viewport.p_maximo.x) / 2
        center_y = (self.viewport.p_minimo.y + self.viewport.p_maximo.y) / 2
        center = Ponto(center_x, center_y)

        # Ajustar as dimensões do viewport
        width = self.viewport.comprimento() * factor
        height = self.viewport.altura() * factor

        # Atualizar as coordenadas do viewport
        self.viewport.p_minimo.x = center_x - width / 2
        self.viewport.p_minimo.y = center_y - height / 2
        self.viewport.p_maximo.x = center_x + width / 2
        self.viewport.p_maximo.y = center_y + height / 2

        for ponto in self.pontos:
            ponto.zoom(factor, center)
        for reta in self.retas:
            reta.a.zoom(factor, center)
            reta.b.zoom(factor, center)
        for poligono in self.poligonos:
            for ponto in poligono.pontos:
                ponto.zoom(factor, center)

        self.update_scene()