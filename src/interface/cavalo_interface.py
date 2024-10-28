import tkinter as tk
from tkinter import PhotoImage, Frame, Label, Tk, Menu, messagebox, simpledialog

from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface

class CavaloInterface(DogPlayerInterface):
    def __init__(self):
        self.status_partida = 'NAO INICIADA'
        self.mainWindow = Tk()
        self.build_mainwindow()

        player_name = simpledialog.askstring(title="Identificar jogador", prompt="Digite o seu nome")
        self.dog_server_interface = DogActor()

        message = f"{self.dog_server_interface.initialize(player_name, self)}!"
        messagebox.showinfo(title="Dog Server", message=message)

        self.mainWindow.mainloop()

    def build_mainwindow(self):
        self.mainWindow.title('Salto do Cavalo')
        self.mainWindow.iconbitmap("images/icon.ico")
        
        self.mainWindow.geometry("675x720")
        self.mainWindow.resizable(False, False)
        self.mainWindow["bg"] = "green"

        self.boardFrame = Frame(self.mainWindow, padx=75, pady=45, bg="green")
        self.messageFrame = Frame(self.mainWindow, padx=4, pady=1, bg="green")

        self.imagemVerde = PhotoImage(file="images/verde.png")
        self.imagemVermelho = PhotoImage(file="images/vermelho.png")
        self.imagemCavaloBranco = PhotoImage(file="images/cavalo-branco.png")
        self.imagemCavaloBrancoEscolhido = PhotoImage(file="images/cavalo-branco-escolhido.png")
        self.imagemCavaloPreto = PhotoImage(file="images/cavalo-preto.png")
        self.imagemCavaloPretoEscolhido = PhotoImage(file="images/cavalo-preto-escolhido.png")

        self.boardView = []
        for linha in range(5):
            labels_linha = []
            for coluna in range(5):
                label = Label(self.boardFrame, bd=2, relief="solid", image=self.imagemVerde)
                label.grid(row=linha, column=coluna)
                label.bind("<Button-1>", lambda event, line=linha, column=coluna: self.select_destination(event, line, column))
                labels_linha.append(label)
            self.boardView.append(labels_linha)

        self.boardView[4][4].config(image=self.imagemCavaloBranco)
        self.boardView[0][0].config(image=self.imagemCavaloPreto)

        self.labelMessage = Label(self.messageFrame, bg="green", text='Vez do Branco', font="arial 14")
        self.labelMessage.grid(row=0, column=0, columnspan=3)
        self.boardFrame.grid(row=0, column=0)
        self.messageFrame.grid(row=1, column=0)

        self.menu = Menu(self.mainWindow)
        self.menu.option_add("*tearOff", tk.FALSE)
        self.mainWindow["menu"] = self.menu

        self.menuOptions = Menu(self.menu, bg="#FFFFFF")
        self.menu.add_cascade(menu=self.menuOptions, label="Menu")
        self.menuOptions.add_command(label="Iniciar partida", command=self.start_match, activebackground="#C5CDE7", activeforeground="#000")
        self.menuOptions.add_command(label="Sair", command=exit, activebackground="#C5CDE7", activeforeground="#000")

        self.selectedPiece = None
        self.selectedImage = None
        self.whiteTurn = True

    def valid_move(self, prev_row, prev_col, curr_row, curr_col):
        row_diff = abs(prev_row - curr_row)
        col_diff = abs(prev_col - curr_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def select_destination(self, event, linha: int, coluna: int):
        label = self.boardView[linha][coluna]

        if self.whiteTurn and label['image'] == str(self.imagemCavaloBranco):
            self.selectedPiece = label
            self.selectedImage = self.imagemCavaloBrancoEscolhido
            label.config(image=self.imagemCavaloBrancoEscolhido)
        elif not self.whiteTurn and label['image'] == str(self.imagemCavaloPreto):
            self.selectedPiece = label
            self.selectedImage = self.imagemCavaloPretoEscolhido
            label.config(image=self.imagemCavaloPretoEscolhido)
        else:
            old_row, old_col = None, None
            for r in range(5):
                for c in range(5):
                    if self.boardView[r][c] == self.selectedPiece:
                        old_row, old_col = r, c

            if label['image'] == str(self.imagemVerde) and self.valid_move(old_row, old_col, linha, coluna):
                if self.whiteTurn:
                    label.config(image=self.imagemCavaloBranco)
                else:
                    label.config(image=self.imagemCavaloPreto)

                self.selectedPiece.config(image=self.imagemVermelho)
                self.whiteTurn = not self.whiteTurn
                self.labelMessage.config(text='Vez do Preto' if not self.whiteTurn else 'Vez do Branco')

                self.selectedPiece = None
                self.selectedImage = None

    def start_match(self):
        if self.status_partida == 'NAO INICIADA':
            start_status = self.dog_server_interface.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()

            if code == "0" or code == "1":
                messagebox.showinfo(message=message)
            elif code == "2":
                jogadores = start_status.get_players()
                print(jogadores)
                messagebox.showinfo(message=message)

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

    def receive_withdrawal_notification(self):
        print("Oponente desistiu da partida. Jogo encerrado.")

CavaloInterface()
