from jogador import Jogador

class Tabuleiro():
    def __init__(self, jogador_local: Jogador, jogador_remoto: Jogador):
        self.posicoes = []
        self.jogador_local = jogador_local
        self.jogador_remoto = jogador_remoto

    def movimentos_possiveis(self, tabuleiro):
        movimentos_possiveis = []
        movimentos_cavalo = [(2, 1), (2, -1), (-2, 1), (-2, -1), 
                             (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in movimentos_cavalo:
            novo_x = self.posicaoAtual.x + dx
            novo_y = self.posicaoAtual.y + dy

            if 0 <= novo_x < len(tabuleiro.posicoes) and 0 <= novo_y < len(tabuleiro.posicoes[0]):
                posicao_destino = tabuleiro.posicoes[novo_x][novo_y]

                if not posicao_destino.bloqueada:
                    movimentos_possiveis.append(posicao_destino)

        return movimentos_possiveis