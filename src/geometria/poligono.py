from geometria.ponto import Ponto
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