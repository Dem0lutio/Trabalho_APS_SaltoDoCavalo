class Jogador():
    def __init__(self, tabuleiro):
        self._nome = ''
        self._cor = ''
        self._tabuleiro = tabuleiro
        self._posicao_atual = None
        self._vencedor = False
        self._turno = False

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, nome: str) -> None:
        self._nome = nome

    @property
    def cor(self) -> str:
        return self._cor

    @cor.setter
    def cor(self, cor: str) -> None:
        self._cor = cor

    @property
    def tabuleiro(self) -> str:
        return self._tabuleiro

    @property
    def posicao_atual(self):
        return self._posicao_atual

    @posicao_atual.setter
    def posicao_atual(self, posicao):
        self._posicao_atual = posicao

    @property
    def vencedor(self) -> bool:
        return self._vencedor

    @vencedor.setter
    def vencedor(self, vencedor: bool) -> None:
        self._vencedor = vencedor

    @property
    def turno(self) -> bool:
        return self._turno

    def trocar_turno(self) -> None:
        self._turno = not self._turno

    def movimentos_possiveis(self) -> list:
        movimentos_possiveis = []
        movimentos_cavalo = [(2, 1), (2, -1), (-2, 1), (-2, -1), 
                             (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in movimentos_cavalo:
            novo_x = self.posicao_atual.x + dx
            novo_y = self.posicao_atual.y + dy

            if 0 <= novo_x <= 4 and 0 <= novo_y <= 4:
                posicao_destino = self.tabuleiro.posicoes[novo_x][novo_y]

                if not posicao_destino.bloqueada:
                    movimentos_possiveis.append(posicao_destino)

        return movimentos_possiveis