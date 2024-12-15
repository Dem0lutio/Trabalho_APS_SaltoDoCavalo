import os
import tkinter as tk
from typing import Dict
from tkinter import PhotoImage, Frame, Label, Tk, Menu, messagebox, simpledialog
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface

from entities.tabuleiro import Tabuleiro

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CavaloInterface(DogPlayerInterface):
    def __init__(self):
        self.janela_principal = Tk()
        self.tabuleiro = Tabuleiro(self)
        self.construir_janela_principal()
        
        player_name = simpledialog.askstring(title="Identificar jogador", prompt="Digite o seu nome")
        self.dog_server_interface = DogActor()
        
        message = f"{self.dog_server_interface.initialize(player_name, self)}!"
        messagebox.showinfo(title="Dog Server", message=message)

        self.janela_principal.mainloop()

    def construir_janela_principal(self):
        self.janela_principal.title('Salto do Cavalo')
        self.janela_principal.iconbitmap("images/icon.ico")
        
        self.janela_principal.geometry("675x720")
        self.janela_principal.resizable(False, False)
        self.janela_principal["bg"] = "green"

        self.quadro_tabuleiro = Frame(self.janela_principal, padx=75, pady=45, bg="green")
        self.quadro_mensagem = Frame(self.janela_principal, padx=4, pady=1, bg="green")

        self.imagem_verde = PhotoImage(file="images/verde.png")
        self.imagem_vermelho = PhotoImage(file="images/vermelho.png")
        self.imagem_cavalo_branco = PhotoImage(file="images/cavalo-branco.png")
        self.imagem_cavalo_branco_escolhido = PhotoImage(file="images/cavalo-branco-escolhido.png")
        self.imagem_cavalo_preto = PhotoImage(file="images/cavalo-preto.png")
        self.imagem_cavalo_preto_escolhido = PhotoImage(file="images/cavalo-preto-escolhido.png")

        self.label_mensagem = Label(self.quadro_mensagem, bg="green", text='Aguardando início de partida...', font="arial 14")
        self.label_mensagem.grid(row=0, column=0, columnspan=3)
        self.quadro_tabuleiro.grid(row=0, column=0)
        self.quadro_mensagem.grid(row=1, column=0)

        self.menu = Menu(self.janela_principal)
        self.menu.option_add("*tearOff", tk.FALSE)
        self.janela_principal["menu"] = self.menu

        self.menuOptions = Menu(self.menu, bg="#FFFFFF")
        self.menu.add_cascade(menu=self.menuOptions, label="Menu")
        self.menuOptions.add_command(label="Iniciar partida", command=self.iniciar_partida, activebackground="#C5CDE7", activeforeground="#000")
        self.menuOptions.add_command(label="Sair", command=exit, activebackground="#C5CDE7", activeforeground="#000")

        self.labels_tabuleiro = []
        for linha in range(5):
            labels_linha = []
            for coluna in range(5):
                label = Label(self.quadro_tabuleiro, bd=2, relief="solid", image=self.imagem_verde)
                label.grid(row=linha, column=coluna)
                label.bind("<Button-1>", lambda event, line=linha, column=coluna: self.selecionar_posicao(event, line, column))
                labels_linha.append(label)
            self.labels_tabuleiro.append(labels_linha)

        self.labels_tabuleiro[4][4]['image'] = self.imagem_cavalo_branco
        self.labels_tabuleiro[0][0]['image'] = self.imagem_cavalo_preto
    
    def selecionar_posicao(self, event, linha: int, coluna: int):
        status_partida = self.tabuleiro.status_partida

        if (status_partida == 'AGUARDANDO SELECAO DO CAVALO' or status_partida == 'AGUARDANDO SELECAO DESTINO'):

            movimento = self.tabuleiro.selecionar_posicao(linha, coluna)

            self.atualizar_interface()

            if movimento is not None:
                self.dog_server_interface.send_move(movimento)

    def iniciar_partida(self):
        if self.tabuleiro.status_partida in ('PARTIDA NAO INICIADA', 'PARTIDA FINALIZADA'):
            start_status = self.dog_server_interface.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()

            if code == "0" or code == "1":
                messagebox.showinfo(message=message)
            elif code == "2":
                jogadores = start_status.get_players()
                self.tabuleiro.iniciar_partida(jogadores)

                self.atualizar_interface()

                messagebox.showinfo(message=message)

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        jogadores = start_status.get_players()
        self.tabuleiro.iniciar_partida(jogadores)

        self.atualizar_interface()

    def receive_move(self, a_move: Dict):
        self.tabuleiro.receber_jogada(a_move)

        self.atualizar_interface()

    def receive_withdrawal_notification(self):
        print("Oponente desistiu da partida. Jogo encerrado.")

    def notificacao(self, mensagem: str):
        messagebox.showinfo(message=mensagem)

    def atualizar_interface(self):
        if self.tabuleiro.status_partida == 'PARTIDA NAO INICIADA':
            self.label_mensagem['text'] = 'Aguardando início de partida...'
        elif self.tabuleiro.status_partida == 'PARTIDA FINALIZADA':
            messagebox.showinfo(message='FIM DE JOGO!')
            self.label_mensagem['text'] = f'FIM DE JOGO! [{self.tabuleiro.get_jogador_atual().nome}] venceu.' if self.tabuleiro.get_jogador_atual().vencedor else f'FIM DE JOGO! [{self.tabuleiro.get_jogador_espera().nome}] venceu' 
        else:
            self.label_mensagem['text'] = f'Vez do Cavalo Branco [{self.tabuleiro.get_jogador_atual().nome}]' if self.tabuleiro.get_jogador_atual().cor == 'BRANCO' else f'Vez do Cavalo Preto [{self.tabuleiro.get_jogador_atual().nome}]' 

        self.temp_labels_tabuleiro = []
        for linha in range(5):
            for coluna in range(5):
                image = ''
                if self.tabuleiro.posicao_ocupada(linha, coluna) == 'CAVALO BRANCO':
                    image = self.imagem_cavalo_branco
                elif self.tabuleiro.posicao_ocupada(linha, coluna) == 'CAVALO BRANCO SELECIONADO':
                    image = self.imagem_cavalo_branco_escolhido
                elif self.tabuleiro.posicao_ocupada(linha, coluna) == 'CAVALO PRETO':
                    image = self.imagem_cavalo_preto
                elif self.tabuleiro.posicao_ocupada(linha, coluna) == 'CAVALO PRETO SELECIONADO':
                    image = self.imagem_cavalo_preto_escolhido
                elif self.tabuleiro.posicao_bloqueada(linha, coluna) and self.tabuleiro.posicao_ocupada(linha, coluna) == '':
                    image = self.imagem_vermelho
                else:
                    image = self.imagem_verde

                self.temp_labels_tabuleiro.append(image)
                self.labels_tabuleiro[linha][coluna]['image'] = self.temp_labels_tabuleiro[-1]