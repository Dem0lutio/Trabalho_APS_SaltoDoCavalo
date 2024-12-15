class Jogador():
    def __init__(self):
        self._nome = ''
        self._cor = ''
        self._posicao_atual = None
        self._vencedor = False
        self._turno = False

    def get_nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome

    def get_cor(self) -> str:
        return self._cor

    def set_cor(self, cor: str) -> None:
        self._cor = cor

    def get_posicao_atual(self):
        return self._posicao_atual

    def set_posicao_atual(self, posicao):
        self._posicao_atual = posicao

    def get_vencedor(self) -> bool:
        return self._vencedor

    def set_vencedor(self, vencedor: bool) -> None:
        self._vencedor = vencedor

    def get_turno(self) -> bool:
        return self._turno

    def set_turno(self, turno: bool) -> None:
        self._turno = turno

    def trocar_turno(self) -> None:
        self._turno = not self._turno
