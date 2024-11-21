class Posicao():
    def __init__(self, x: int, y: int):

        self._x = x
        self._y = y
        self._blocked = False if ((x == 4 and y == 4) or (x == 0 and y == 0)) else True

        @property
        def x(self) -> int:
            return self._x

        @x.setter
        def x(self, x: int) -> None:
            self._x = x

        @property
        def y(self) -> int:
            return self._y

        @y.setter
        def y(self, y: int) -> None:
            self._y = y

        @property
        def blocked(self) -> bool:
            return self._blocked

        @blocked.setter
        def blocked(self, blocked: bool) -> None:
            self._blocked = blocked


        def position_reachable(self, current_position, target_position):
            dx = abs(current_position.x - target_position.x)
            dy = abs(current_position.y - target_position.y)

            if target_position.blocked:
                return False

            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)