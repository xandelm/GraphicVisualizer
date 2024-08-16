import math
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
    
    def rotate(self, angle_degrees: float, center: 'Ponto' = None) -> None:
        angle_radians = math.radians(angle_degrees)
        
        if center is None:
            center = Ponto(0, 0)


        # Translate point back to origin
        translated_x = self._x - center.x
        translated_y = self._y - center.y

        # Apply rotation matrix
        x_new = translated_x * math.cos(angle_radians) - translated_y * math.sin(angle_radians)
        y_new = translated_x * math.sin(angle_radians) + translated_y * math.cos(angle_radians)

        # Translate point back
        self._x = x_new + center.x
        self._y = y_new + center.y

    def zoom(self, factor: float, center: 'Ponto') -> None:
        self._x = center.x + (self._x - center.x) * factor
        self._y = center.y + (self._y - center.y) * factor
