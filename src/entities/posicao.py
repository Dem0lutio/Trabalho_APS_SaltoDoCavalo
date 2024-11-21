class Posicao():
    def __init__(self, x: int, y: int):

        self._x = x
        self._y = y
        self._bloqueada = True if ((x == 4 and y == 4) or (x == 0 and y == 0)) else False

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
        def bloqueada(self) -> bool:
            return self._bloqueada

        @bloqueada.setter
        def bloqueada(self, bloqueada: bool) -> None:
            self._bloqueada = bloqueada

        def posicao_alcancavel(self, posicao_atual: Posicao, posicao_destino: Posicao) -> bool:
            """
                Retorna se é possível o jogador se movimentar para a posição selecionada.

                :param posicao_atual: Posição atual do jogador no tabuleiro.
                :param posicao_destino: Posição destino selecionada pelo jogador.
                :return: Booleano indicando se a posição é alcançável.
            """

            dx = abs(posicao_atual.x - posicao_destino.x)
            dy = abs(posicao_atual.y - posicao_destino.y)

            if posicao_destino.bloqueada:
                return False

            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)