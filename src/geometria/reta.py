from geometria.ponto import Ponto
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