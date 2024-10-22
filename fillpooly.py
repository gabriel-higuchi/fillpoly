import tkinter as tk
from tkinter import colorchooser

class PoligonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desenhar Polígono")

        # Canvas para desenhar
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Variáveis
        self.pontos = []  # Lista para armazenar os pontos atuais
        self.pontos_ids = []  # Lista para armazenar os IDs dos círculos (pontos)
        self.poligonos = []  # Lista para armazenar IDs dos polígonos desenhados
        self.linhas_preenchimento = {}  # Dicionário para armazenar linhas de preenchimento por polígono
        self.cor_aresta = "yellow"  # Cor padrão das arestas
        self.cor_preencher = "lightblue"  # Cor padrão de preenchimento
        self.poligono_selecionado = None  # ID do polígono selecionado para excluir
        self.contador_poligonos = 0  # Contador de polígonos
        self.botao_poligonos = {}  # Dicionário para armazenar os botões dos polígonos

        # Frame para botões dos polígonos
        self.frame_poligonos = tk.Frame(self.root)
        self.frame_poligonos.pack()

        # Frame de botões
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()

        # Botões de controle
        self.botao_cor_aresta = tk.Button(self.frame_botoes, text="Mudar Cor da aresta", command=self.mudar_cor_aresta)
        self.botao_cor_aresta.grid(row=0, column=0, padx=5, pady=5)

        self.botao_cor_preencher = tk.Button(self.frame_botoes, text="Mudar Cor de Preenchimento", command=self.mudar_cor_preencher)
        self.botao_cor_preencher.grid(row=1, column=1, padx=5, pady=5)

        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir", command=self.excluir_poligono)
        self.botao_excluir.grid(row=0, column=1, padx=5, pady=5)

        self.botao_limpar = tk.Button(self.frame_botoes, text="Limpar Tudo", command=self.limpar_canvas)
        self.botao_limpar.grid(row=0, column=2, padx=5, pady=5)

        # Eventos de clique no canvas
        self.canvas.bind("<Button-1>", self.adicionar_ponto)  # Clique simples para adicionar pontos
        self.canvas.bind("<Double-1>", self.fechar_poligono)  # Duplo clique para fechar o polígono

    def adicionar_ponto(self, event):
        """Adiciona um ponto e desenha-o no canvas."""
          # Permite adicionar pontos apenas se não estiver no modo de seleção
        x, y = event.x, event.y
        self.pontos.append((x, y))
        raio = 3
        ponto_id = self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill='black')
        self.pontos_ids.append(ponto_id)  # Armazena o ID do ponto
        print(f"Adicionando ponto ({x}, {y})")

    def fechar_poligono(self, event):
        """Fecha o polígono e armazena seu ID."""
        self.pontos_ids.extend(self.pontos)  # Adiciona os IDs dos pontos à lista de IDs
        if len(self.pontos) > 2:
            # Desenha o polígono e armazena seu ID
            poligono_id = self.canvas.create_polygon(
                self.pontos, outline=self.cor_aresta, fill='', width=2
            )
            self.poligonos.append(poligono_id)  # Armazena o ID do polígono

            print("poligono:", self.poligonos)
            print(f"Vértices: {self.pontos}")

            # Calcular coeficientes angulares
            self.preencher_poligono(self.pontos, poligono_id)  # Passa o ID do polígono

            self.pontos.clear()  # Limpa os pontos para um novo polígono
            self.contador_poligonos += 1
            nome_poligono = f"Polígono {self.contador_poligonos}"
            botao_poligono = tk.Button(self.frame_poligonos, text=nome_poligono, 
                                       command=lambda pid=poligono_id: self.selecionar_por_botao(pid))
            botao_poligono.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
            self.botao_poligonos[poligono_id] = botao_poligono  # Armazena o botão no dicionário

    def preencher_poligono(self, pontos, poligono_id):
        """Preenche o polígono no canvas usando o algoritmo Scanline Fill."""
        # Determina os limites verticais (y_min e y_max) do polígono
        y_min = min(p[1] for p in pontos)
        y_max = max(p[1] for p in pontos)

        # Dicionário para armazenar as interseções em cada scanline
        intersecoes = {y: [] for y in range(y_min, y_max + 1)}

        # Calcula as interseções de cada aresta com as scanlines
        num_pontos = len(pontos)
        for i in range(num_pontos):
            x1, y1 = pontos[i]
            x2, y2 = pontos[(i + 1) % num_pontos]  # Conecta o último ponto ao primeiro

            # Ignora arestas horizontais
            if y1 != y2:
                # Garante que a aresta sempre vá de y_min para y_max
                if y1 > y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1

                # Calcula o incremento Tx (baseado na inclinação)
                dx = x2 - x1
                dy = y2 - y1
                Tx = dx / dy  # Incremento de x para cada variação em y

                # Inicia em x1 e percorre de y1 até y2
                x = x1
                for y in range(y1, y2 + 1):
                    intersecoes[y].append(x)
                    x += Tx  # Incrementa x para a próxima scanline

        # Preenche o polígono desenhando linhas entre pares de interseções
        self.linhas_preenchimento[poligono_id] = []  # Inicializa a lista de linhas para o novo polígono
        for y, pontos_x in intersecoes.items():
            pontos_x.sort()  # Ordena as interseções em ordem crescente

            # Desenha uma linha para cada par de interseções
            for i in range(0, len(pontos_x) - 1, 2):
                x_ini = round(pontos_x[i])
                x_fim = round(pontos_x[i + 1])
                linha_id = self.canvas.create_line(x_ini, y, x_fim, y, fill=self.cor_preencher)
                self.linhas_preenchimento[poligono_id].append(linha_id)  # Armazena o ID da linha de preenchimento
                print(f"Preenchendo scanline em y = {y} de x = {x_ini} até x = {x_fim}") 

        print("Polígono preenchido com sucesso.")

    def selecionar_por_botao(self, poligono_id):
        """Seleciona o polígono correspondente ao botão clicado.""" 
        self.poligono_selecionado = poligono_id
        self.canvas.itemconfig(poligono_id, outline='red')

    def mudar_cor_preencher(self):
        """Abre um seletor de cores para escolher a cor de preenchimento."""    
        nova_cor = colorchooser.askcolor(title="Escolher Cor de Preenchimento")[1]
        if nova_cor:
            self.cor_preencher = nova_cor

    def remover_pontos(self, pontos):
        """Remove os pontos do polígono do canvas."""
        for ponto_id in self.pontos_ids:
            self.canvas.delete(ponto_id)  # Remove o ponto do canvas
        self.pontos_ids.clear()  # Limpa a lista de IDs dos pontos

            
    def mudar_cor_aresta(self):
        """Abre um seletor de cores para escolher a cor das arestas."""
        nova_cor = colorchooser.askcolor(title="Escolher Cor da Aresta")[1]
        if nova_cor:
            self.cor_aresta = nova_cor

    def excluir_poligono(self):
        if self.poligono_selecionado:
            # Verifica se o polígono selecionado está na lista antes de removê-lo
            if self.poligono_selecionado in self.poligonos:
                # Remove os pontos associados ao polígono
                self.remover_pontos(self.pontos)  # Limpa os pontos do canvas

                self.canvas.delete(self.poligono_selecionado)  # Exclui o polígono do canvas
                self.poligonos.remove(self.poligono_selecionado)  # Remove o ID da lista

                # Remove as linhas de preenchimento associadas ao polígono
                if self.poligono_selecionado in self.linhas_preenchimento:
                    for linha_id in self.linhas_preenchimento[self.poligono_selecionado]:
                        self.canvas.delete(linha_id)  # Remove a linha do canvas

                    del self.linhas_preenchimento[self.poligono_selecionado]  # Remove as linhas de preenchimento

                # Remove o botão correspondente ao polígono
                if self.poligono_selecionado in self.botao_poligonos:
                    botao = self.botao_poligonos[self.poligono_selecionado]
                    botao.destroy()  # Remove o botão da interface
                    del self.botao_poligonos[self.poligono_selecionado]  # Remove do dicionário de botões

                self.poligono_selecionado = None


    def limpar_canvas(self):
        """Limpa todo o canvas e reinicia as variáveis."""
        self.canvas.delete("all")
        self.pontos.clear()
        self.poligonos.clear()
        self.poligono_selecionado = None
        self.modo_selecao = False  # Reseta o modo de seleção

# Inicializa a interface
if __name__ == "__main__":
    root = tk.Tk()
    app = PoligonoApp(root)
    root.mainloop()
