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
        status_partida = self.tabuleiro.get_status_partida()

        if status_partida in ('AGUARDANDO SELECAO DO CAVALO', 'AGUARDANDO SELECAO DESTINO'):

            movimento = self.tabuleiro.selecionar_posicao(linha, coluna)

            self.atualizar_interface()

            if movimento is not None:
                self.dog_server_interface.send_move(movimento)

    def iniciar_partida(self):
        if self.tabuleiro.get_status_partida() in ('PARTIDA NAO INICIADA', 'PARTIDA FINALIZADA'):
            start_status = self.dog_server_interface.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()

            if code in ("0", "1"):
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
        self.tabuleiro.receber_abandono_partida()
        message = 'A partida foi abandonada pelo oponente!'
        messagebox.showinfo(title='Partida encerrada!', message=message)
        self.atualizar_interface()

    def notificacao(self, mensagem: str):
        messagebox.showinfo(message=mensagem)

    def atualizar_interface(self):
        if self.tabuleiro.get_status_partida() == 'PARTIDA NAO INICIADA':
            self.label_mensagem['text'] = 'Aguardando início de partida...'
        elif self.tabuleiro.get_status_partida() == 'PARTIDA FINALIZADA':
            vencedor = self.tabuleiro.get_jogador_atual().get_nome() if self.tabuleiro.get_jogador_atual().get_vencedor() else self.tabuleiro.get_jogador_espera().get_nome()
            self.label_mensagem['text'] = f'Partida encerrada! [{vencedor}] venceu.'
        elif self.tabuleiro.get_status_partida() == 'PARTIDA ABANDONADA':
            self.label_mensagem['text'] = 'Partida encerrada! O oponente abandonou a partida'
        else:
            jogador_atual = self.tabuleiro.get_jogador_atual()
            cor = jogador_atual.get_cor()
            nome = jogador_atual.get_nome()
            self.label_mensagem['text'] = f"Vez do Cavalo {'Branco' if cor == 'BRANCO' else 'Preto'} [{nome}]"

        for linha in range(5):
            for coluna in range(5):
                posicao = self.tabuleiro.get_posicoes()[linha][coluna]
                image = ''
                if posicao.get_ocupada() == 'CAVALO BRANCO':
                    image = self.imagem_cavalo_branco
                elif posicao.get_ocupada() == 'CAVALO BRANCO SELECIONADO':
                    image = self.imagem_cavalo_branco_escolhido
                elif posicao.get_ocupada() == 'CAVALO PRETO':
                    image = self.imagem_cavalo_preto
                elif posicao.get_ocupada() == 'CAVALO PRETO SELECIONADO':
                    image = self.imagem_cavalo_preto_escolhido
                elif posicao.get_bloqueada() and posicao.get_ocupada() == '':
                    image = self.imagem_vermelho
                else:
                    image = self.imagem_verde

                self.labels_tabuleiro[linha][coluna]['image'] = image
