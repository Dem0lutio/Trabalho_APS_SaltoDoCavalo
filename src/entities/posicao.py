class Posicao():
    def __init__(self, x: int, y: int):

        self._x = x
        self._y = y
        self._blocked = True if ((x == 4 and y == 4) or (x == 0 and y == 0)) else False

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

        def position_reachable(self, current_position: Posicao, target_position: Posicao) -> bool:
            """
                Retorna se é possível o jogador se movimentar para a posição selecionada.

                :param current_position: Posição atual do jogador no tabuleiro.
                :param target_position: Posição destino selecionada pelo jogador.
                :return: Booleano indicando se a posição é alcançável.
            """

            dx = abs(current_position.x - target_position.x)
            dy = abs(current_position.y - target_position.y)

            if target_position.blocked:
                return False

            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)