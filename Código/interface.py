from tkinter import *

class SaltoDoCavaloInterface:
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Salto do Cavalo")
		self.mainWindow.iconbitmap("images/icon.ico")
		self.mainWindow.geometry("675x720")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"] = "gray"

		self.mainFrame = Frame(self.mainWindow, padx=75, pady=45, bg="gray")
		self.messageFrame = Frame(self.mainWindow, padx=4, pady=1, bg="gray")

		# Imagens
		self.imagemVerde = PhotoImage(file="images/verde.png")
		self.imagemVermelho = PhotoImage(file="images/vermelho.png")
		self.imagemCavaloBranco = PhotoImage(file="images/cavalo-branco.png")
		self.imagemCavaloBrancoEscolhido = PhotoImage(file="images/cavalo-branco-escolhido.png")
		self.imagemCavaloPreto = PhotoImage(file="images/cavalo-preto.png")
		self.imagemCavaloPretoEscolhido = PhotoImage(file="images/cavalo-preto-escolhido.png")

		# Monta a imagem do tabuleiro
		self.boardView = []
		for y in range(5):
			viewTier = []
			for x in range(5):
				aLabel = Label(self.mainFrame, bd=2, relief="solid", image=self.imagemVerde)
				aLabel.grid(row=x, column=y)
				aLabel.bind("<Button-1>", lambda event, line=y+1, column=x+1: self.click(event, line, column))
				viewTier.append(aLabel)
			self.boardView.append(viewTier)

		# Adiciona o cavalo branco na posição 5,5 (índice 4,4 na lista)
		self.boardView[4][4].config(image=self.imagemCavaloBranco)

		# Adiciona o cavalo preto na posição 0,0 (índice 0,0 na lista)
		self.boardView[0][0].config(image=self.imagemCavaloPreto)

		# Mensagem de estado
		self.labelMessage = Label(self.messageFrame, bg="gray", text='Vez do Branco', font="arial 14")
		self.labelMessage.grid(row=0, column=0, columnspan=3)
		self.mainFrame.grid(row=0, column=0)
		self.messageFrame.grid(row=1, column=0)

		# Variáveis para armazenar o cavalo selecionado
		self.selectedPiece = None
		self.selectedImage = None

		# Controla de quem é a vez
		self.whiteTurn = True # Começa com o branco

		self.mainWindow.mainloop()

	def is_valid_move(self, old_row, old_col, new_row, new_col):
		# Verifica se a movimentação é válida em formato L
		row_diff = abs(old_row - new_row)
		col_diff = abs(old_col - new_col)
		return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

	def click(self, event, linha, coluna):
		label = self.boardView[linha-1][coluna-1]

		# Se não houver cavalo selecionado, verificar se clicou no cavalo da vez
		if self.selectedPiece is None:
			if self.whiteTurn and label['image'] == str(self.imagemCavaloBranco):
				# Selecionar cavalo branco
				self.selectedPiece = label
				self.selectedImage = self.imagemCavaloBrancoEscolhido  # Usar a imagem do cavalo branco escolhido
				label.config(image=self.imagemCavaloBrancoEscolhido)  # Mudar a imagem para o cavalo branco escolhido
			elif not self.whiteTurn and label['image'] == str(self.imagemCavaloPreto):
				# Selecionar cavalo preto
				self.selectedPiece = label
				self.selectedImage = self.imagemCavaloPretoEscolhido  # Usar a imagem do cavalo preto escolhido
				label.config(image=self.imagemCavaloPretoEscolhido)  # Mudar a imagem para o cavalo preto escolhido
		# Se já houver um cavalo selecionado, tentar movê-lo para a nova posição
		else:
			old_row, old_col = None, None
			# Procurar a posição do cavalo selecionado
			for r in range(5):
				for c in range(5):
					if self.boardView[r][c] == self.selectedPiece:
						old_row, old_col = r, c

			if label['image'] == str(self.imagemVerde) and self.is_valid_move(old_row, old_col, linha-1, coluna-1):  # Movimentar em L
				# Atualizar a posição do cavalo com a imagem original (não escolhida)
				if self.whiteTurn:
					label.config(image=self.imagemCavaloBranco)  # Movendo cavalo branco
				else:
					label.config(image=self.imagemCavaloPreto)  # Movendo cavalo preto

				# Voltar a casa anterior para o estado "vermelho"
				self.selectedPiece.config(image=self.imagemVermelho)

				# Alternar turno
				self.whiteTurn = not self.whiteTurn
				self.labelMessage.config(text='Vez do Preto' if not self.whiteTurn else 'Vez do Branco')

				# Limpar a seleção
				self.selectedPiece = None
				self.selectedImage = None

SaltoDoCavaloInterface()
