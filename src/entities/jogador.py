from posicao import Posicao

class Jogador():
    def __init__(self):
        
        self._nome = ''
        self._cor = ''
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

    @turno.setter
    def turno(self, turno: bool) -> None:
        self._turno = turno