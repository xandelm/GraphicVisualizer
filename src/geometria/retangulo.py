from geometria.ponto import Ponto
class Retangulo():
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