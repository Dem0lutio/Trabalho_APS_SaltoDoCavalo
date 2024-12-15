class Posicao():
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._ocupada = ''
        self._bloqueada = False

    def get_x(self) -> int:
        return self._x

    def set_x(self, x: int) -> None:
        self._x = x

    def get_y(self) -> int:
        return self._y

    def set_y(self, y: int) -> None:
        self._y = y

    def get_bloqueada(self) -> bool:
        return self._bloqueada

    def set_bloqueada(self, bloqueada: bool) -> None:
        self._bloqueada = bloqueada

    def get_ocupada(self) -> bool:
        return self._ocupada

    def set_ocupada(self, ocupada: bool) -> None:
        self._ocupada = ocupada

    def posicao_alcancavel(self, posicao_destino) -> bool:
        
        dx = abs(self.get_x() - posicao_destino.get_x())
        dy = abs(self.get_y() - posicao_destino.get_y())

        if posicao_destino.get_bloqueada():
            return False

        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
