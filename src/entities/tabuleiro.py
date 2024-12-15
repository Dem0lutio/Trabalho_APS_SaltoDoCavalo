from typing import Dict, Union
from entities.jogador import Jogador
from entities.posicao import Posicao

class Tabuleiro():
    def __init__(self, interface):
        self._posicoes = []
        self._status_partida = 'PARTIDA NAO INICIADA'
        self._interface = interface
        self._jogador_local = Jogador()
        self._jogador_remoto = Jogador()

        for linha in range(5):
            coluna_posicoes = []
            for coluna in range(5):
                coluna_posicoes.append(Posicao(linha, coluna))
            self._posicoes.append(coluna_posicoes)

    def get_posicoes(self):
        return self._posicoes

    def get_status_partida(self):
        return self._status_partida

    def set_status_partida(self, status_partida: str):
        self._status_partida = status_partida

    def iniciar_partida(self, jogadores: list[str]) -> None:
        self._jogador_local.set_nome(jogadores[0][0])
        self._jogador_remoto.set_nome(jogadores[1][0])

        if jogadores[0][2] == '1':
            self._jogador_local.set_cor('BRANCO')
            self._jogador_remoto.set_cor('PRETO')
            self._jogador_local.trocar_turno()
            self.set_status_partida('AGUARDANDO SELECAO DO CAVALO')
        else:
            self._jogador_local.set_cor('PRETO')
            self._jogador_remoto.set_cor('BRANCO')
            self._jogador_remoto.trocar_turno()
            self.set_status_partida('AGUARDANDO JOGADOR REMOTO')

        self.posicoes_iniciais()

    def posicoes_iniciais(self):
        for linha in range(5):
            for coluna in range(5):
                self._posicoes[linha][coluna].set_bloqueada(False)
                self._posicoes[linha][coluna].set_ocupada('')

        self._posicoes[4][4].set_bloqueada(True)
        self._posicoes[4][4].set_ocupada('CAVALO BRANCO')
        self._posicoes[0][0].set_bloqueada(True)
        self._posicoes[0][0].set_ocupada('CAVALO PRETO')

        if self._jogador_local.get_cor() == 'BRANCO':
            self._jogador_local.set_posicao_atual(self._posicoes[4][4])
            self._jogador_remoto.set_posicao_atual(self._posicoes[0][0])
        else:
            self._jogador_local.set_posicao_atual(self._posicoes[0][0])
            self._jogador_remoto.set_posicao_atual(self._posicoes[4][4])

    def selecionar_posicao(self, linha: int, coluna: int) -> Union[Dict, None]:
        status_partida = self.get_status_partida()
        posicao_selecionada = self.get_posicoes()[linha][coluna]

        if status_partida == 'AGUARDANDO SELECAO DO CAVALO':
            return self.selecionar_posicao_origem(posicao_selecionada)
        elif status_partida == 'AGUARDANDO SELECAO DESTINO':
            return self.selecionar_posicao_destino(posicao_selecionada)

    def selecionar_posicao_origem(self, posicao_selecionada: Posicao) -> None:
        jogador_atual = self.get_jogador_atual()

        if posicao_selecionada == jogador_atual.get_posicao_atual():
            self.set_status_partida('AGUARDANDO SELECAO DESTINO')
            if jogador_atual.get_cor() == 'BRANCO':
                posicao_selecionada.set_ocupada('CAVALO BRANCO SELECIONADO')
            else:
                posicao_selecionada.set_ocupada('CAVALO PRETO SELECIONADO')
        else:
            self._interface.notificacao('Você deve selecionar o seu respectivo cavalo!')

    def selecionar_posicao_destino(self, posicao_selecionada: Posicao) -> Union[Dict, None]:
        jogador_atual = self.get_jogador_atual()

        posicao_origem = jogador_atual.get_posicao_atual()
        posicao_destino = posicao_selecionada

        if not posicao_destino.get_bloqueada():
            if posicao_origem.posicao_alcancavel(posicao_destino):
                jogada = {
                    'linha_origem': posicao_origem.get_x(),
                    'coluna_origem': posicao_origem.get_y(),
                    'linha_destino': posicao_destino.get_x(),
                    'coluna_destino': posicao_destino.get_y(),
                    'tipo': 'jogada'
                }

                if jogador_atual.get_cor() == 'BRANCO':
                    posicao_destino.set_ocupada('CAVALO BRANCO')
                    posicao_destino.set_bloqueada(True)
                else:
                    posicao_destino.set_ocupada('CAVALO PRETO')
                    posicao_destino.set_bloqueada(True)

                posicao_origem.set_ocupada('')
                jogador_atual.set_posicao_atual(posicao_destino)

                self._jogador_local.trocar_turno()
                self._jogador_remoto.trocar_turno()

                jogador_atual = self.get_jogador_atual()

                if self.verifica_vencedor():
                    self.set_status_partida('PARTIDA FINALIZADA')
                    jogada['match_status'] = 'finished'
                else:
                    if jogador_atual == self._jogador_local:
                        self.set_status_partida('AGUARDANDO SELECAO DO CAVALO')
                    else:
                        self.set_status_partida('AGUARDANDO JOGADOR REMOTO')
                    jogada['match_status'] = 'next'
                return jogada
            else:
                self._interface.notificacao('A posição escolhida está fora do alcance!')
        else:
            self._interface.notificacao('A posição escolhida está bloqueada!')
    
    def receber_jogada(self, jogada: Dict) -> None:
        if jogada['tipo'] == "jogada":
            self.selecionar_posicao_origem(self.get_posicoes()[jogada['linha_origem']][jogada['coluna_origem']])
            self.selecionar_posicao_destino(self.get_posicoes()[jogada['linha_destino']][jogada['coluna_destino']])
    
    def movimentos_possiveis(self, jogador: Jogador) -> list:
        movimentos_possiveis = []
        movimentos_cavalo = [[2, 1], [2, -1], [-2, 1], [-2, -1], 
                             [1, 2], [1, -2], [-1, 2], [-1, -2]]

        for dx, dy in movimentos_cavalo:
            novo_x = jogador.get_posicao_atual().get_x() + dx
            novo_y = jogador.get_posicao_atual().get_y() + dy

            if 0 <= novo_x <= 4 and 0 <= novo_y <= 4:
                posicao_destino = self._posicoes[novo_x][novo_y]

                if not posicao_destino.get_bloqueada():
                    movimentos_possiveis.append(posicao_destino)

        return movimentos_possiveis

    def verifica_vencedor(self):
        if not self.movimentos_possiveis(self._jogador_local):
            self._jogador_remoto.set_vencedor(True)
            return True
        if not self.movimentos_possiveis(self._jogador_remoto):
            self._jogador_local.set_vencedor(True)
            return True

        return False

    def posicao_bloqueada(self, linha: int, coluna: int) -> bool:
        return self._posicoes[linha][coluna].get_bloqueada()

    def posicao_ocupada(self, linha: int, coluna: int) -> str:
        return self._posicoes[linha][coluna].get_ocupada()

    def get_jogador_atual(self) -> Jogador:
        return self._jogador_local if self._jogador_local.get_turno() else self._jogador_remoto

    def get_jogador_espera(self) -> Jogador:
        return self._jogador_remoto if self._jogador_local.get_turno() else self._jogador_local
