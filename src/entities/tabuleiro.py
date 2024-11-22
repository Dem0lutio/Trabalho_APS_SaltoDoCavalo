from typing import Dict, Union

from entities.jogador import Jogador
from entities.posicao import Posicao

class Tabuleiro():
    def __init__(self, interface):
        self._posicoes = []
        self._status_partida = 'PARTIDA NAO INICIADA'
        self._interface = interface
        self._jogador_local = Jogador(self)
        self._jogador_remoto = Jogador(self)

        for linha in range(5):
            coluna_posicoes = []
            for coluna in range(5):
                coluna_posicoes.append(Posicao(linha, coluna))
            self._posicoes.append(coluna_posicoes)

    @property
    def posicoes(self):
        return self._posicoes
    
    @property
    def status_partida(self):
        return self._status_partida
    
    @status_partida.setter
    def status_partida(self, status_partida: str):
        self._status_partida = status_partida
    
    def iniciar_partida(self, jogadores: list[str]) -> None:
        self._jogador_local.nome = jogadores[0][0]
        self._jogador_remoto.nome = jogadores[1][0]
        
        if jogadores[0][2] == '1':
            self._jogador_local.cor = 'BRANCO'
            self._jogador_remoto.cor = 'PRETO'
            self._jogador_local.trocar_turno()
            self.status_partida = 'AGUARDANDO SELECAO DO CAVALO'
        else:
            self._jogador_local.cor = 'PRETO'
            self._jogador_remoto.cor = 'BRANCO'
            self._jogador_remoto.trocar_turno()
            self.status_partida = 'AGUARDANDO JOGADOR REMOTO'

        self.posicoes_iniciais()

    def posicoes_iniciais(self):

        for linha in range(5):
            for coluna in range(5):
                self._posicoes[linha][coluna].bloqueada = False
                self._posicoes[linha][coluna].ocupada = ''

        self._posicoes[4][4].bloqueada = True
        self._posicoes[4][4].ocupada = 'CAVALO BRANCO'
        self._posicoes[0][0].bloqueada = True
        self._posicoes[0][0].ocupada = 'CAVALO PRETO'

        if self._jogador_local.cor == 'BRANCO':
            self._jogador_local.posicao_atual = self._posicoes[4][4]
            self._jogador_remoto.posicao_atual = self._posicoes[0][0]
        else:
            self._jogador_local.posicao_atual = self._posicoes[0][0]
            self._jogador_remoto.posicao_atual = self._posicoes[4][4]

    def selecionar_posicao(self, linha: int, coluna: int) -> Union[Dict, None]:
        status_partida = self.status_partida
        
        posicao_selecionada = self.posicoes[linha][coluna]

        if status_partida == 'AGUARDANDO SELECAO DO CAVALO':
            return self.selecionar_posicao_origem(posicao_selecionada)
        elif status_partida == 'AGUARDANDO SELECAO DESTINO':
            return self.selecionar_posicao_destino(posicao_selecionada)
        
    def selecionar_posicao_origem(self, posicao_selecionada: Posicao) -> None:
        jogador_atual = self.get_jogador_atual()
        
        if posicao_selecionada == jogador_atual.posicao_atual:
            self.status_partida = 'AGUARDANDO SELECAO DESTINO'
            if jogador_atual.cor == 'BRANCO':
                posicao_selecionada.ocupada = 'CAVALO BRANCO SELECIONADO'
            else:
                posicao_selecionada.ocupada = 'CAVALO PRETO SELECIONADO'
        else:
            self._interface.notificacao('Você deve selecionar o seu respectivo cavalo!')

    def selecionar_posicao_destino(self, posicao_selecionada: Posicao) -> Union[Dict, None]:
        jogador_atual = self.get_jogador_atual()
        
        posicao_origem = jogador_atual.posicao_atual
        posicao_destino = posicao_selecionada

        if not self.posicao_bloqueada(posicao_destino.x, posicao_destino.y):

            if posicao_destino.posicao_alcancavel(posicao_origem, posicao_destino):
                jogada = {'linha_origem': posicao_origem.x,
                          'coluna_origem': posicao_origem.y,
                          'linha_destino': posicao_destino.x,
                          'coluna_destino': posicao_destino.y,
                          'tipo': 'jogada'}
                
                if jogador_atual.cor == 'BRANCO':
                    posicao_destino.ocupada = 'CAVALO BRANCO'
                    posicao_destino.bloqueada = True
                else:
                    posicao_destino.ocupada = 'CAVALO PRETO'
                    posicao_destino.bloqueada = True
                posicao_origem.ocupada = ''
                jogador_atual.posicao_atual = posicao_destino

                self._jogador_local.trocar_turno()
                self._jogador_remoto.trocar_turno()

                jogador_atual = self.get_jogador_atual()

                if self.verifica_vencedor():
                    self.status_partida = 'PARTIDA FINALIZADA'
                    jogada['match_status'] = 'finished'
                else:
                    if jogador_atual == self._jogador_local:
                        self.status_partida = 'AGUARDANDO SELECAO DO CAVALO'
                    else:
                        self.status_partida = 'AGUARDANDO JOGADOR REMOTO'
                    jogada['match_status'] = 'next'
                return jogada
            else:
                self._interface.notificacao('A posição escolhida está fora do alcance!')
        else:
            self._interface.notificacao('A posição escolhida está bloqueada!')

    def receber_jogada(self, jogada: Dict) -> None:
        if jogada['tipo'] == "jogada":
            self.selecionar_posicao_origem(self.posicoes[jogada['linha_origem']][jogada['coluna_origem']])
            self.selecionar_posicao_destino(self.posicoes[jogada['linha_destino']][jogada['coluna_destino']])

    def verifica_vencedor(self):
        if self._jogador_local.turno:
            return True if not self._jogador_local.movimentos_possiveis() else False
        else:
            return True if not self._jogador_remoto.movimentos_possiveis() else False
            
    def posicao_bloqueada(self, linha: int, coluna: int) -> bool:
        return self._posicoes[linha][coluna].bloqueada
    
    def posicao_ocupada(self, linha: int, coluna: int) -> str:
        return self._posicoes[linha][coluna].ocupada
    
    def get_jogador_atual(self) -> Jogador:
        return self._jogador_local if self._jogador_local.turno else self._jogador_remoto