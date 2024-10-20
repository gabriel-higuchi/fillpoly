import tkinter as tk
from tkinter import colorchooser  # Para escolher cores
import random

class PoligonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desenhar Polígono")

        # Canvas para desenhar
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Variáveis
        self.pontos = []  # Lista para armazenar os pontos
        self.cor_aresta = "blue"  # Cor padrão da aresta

        # Botões
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()

        self.botao_limpar = tk.Button(self.frame_botoes, text="Limpar", command=self.limpar_canvas)
        self.botao_limpar.grid(row=0, column=0, padx=5, pady=5)

        self.botao_cor = tk.Button(self.frame_botoes, text="Mudar Cor", command=self.mudar_cor)
        self.botao_cor.grid(row=0, column=1, padx=5, pady=5)

        # Eventos de clique
        self.canvas.bind("<Button-1>", self.adicionar_ponto)  # Clique simples
        self.canvas.bind("<Double-1>", self.fechar_poligono)  # Duplo clique

    def adicionar_ponto(self, event):
        """Adiciona um ponto na lista e desenha no canvas."""
        x, y = event.x, event.y
        self.pontos.append((x, y))

        raio = 3  # Tamanho do ponto
        self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill='black')

    def fechar_poligono(self, event):
        """Fecha o polígono e conecta o último ponto ao primeiro."""
        if len(self.pontos) > 2:
            # Desenha o polígono com a cor atual das arestas
            self.canvas.create_polygon(self.pontos, outline=self.cor_aresta, fill='', width=2)
            self.pontos.clear()  # Limpa os pontos para um novo polígono

    def limpar_canvas(self):
        """Limpa todo o conteúdo do canvas."""
        self.canvas.delete("all")
        self.pontos.clear()

    def mudar_cor(self):
        """Abre um seletor de cores e muda a cor da aresta."""
        nova_cor = colorchooser.askcolor(title="Escolher Cor")[1]  # [1] para obter a cor hexadecimal
        if nova_cor:
            self.cor_aresta = nova_cor

# Inicializa a interface
if __name__ == "__main__":
    root = tk.Tk()
    app = PoligonoApp(root)
    root.mainloop()
