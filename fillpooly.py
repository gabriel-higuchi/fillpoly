import tkinter as tk
from tkinter import colorchooser

class PoligonoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desenhar Polígono")

        # Frame principal para o canvas
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(side=tk.LEFT)

        # Canvas para desenhar
        self.canvas = tk.Canvas(self.frame_principal, width=800, height=600, bg='white')
        self.canvas.pack()

        # Frame lateral para botões
        self.frame_lateral = tk.Frame(self.root)
        self.frame_lateral.pack(side=tk.RIGHT, fill=tk.Y)

        # Variáveis
        self.pontos = []  # Lista para armazenar os pontos atuais
        self.pontos_ids = []  # IDs dos círculos (pontos)
        self.poligonos = []  # IDs dos polígonos desenhados
        self.linhas_preenchimento = {}  # Linhas de preenchimento por polígono
        self.cor_aresta = "yellow"  # Cor padrão das arestas
        self.cor_preencher = "lightblue"  # Cor padrão de preenchimento
        self.poligono_selecionado = None  # ID do polígono selecionado
        self.dados_poligonos = {}  # Armazena dados de cada polígono
        self.contador_poligonos = 0  # Contador de polígonos
        self.botao_poligonos = {}  # Botões dos polígonos
        self.exibir_arestas = True

        # Frame para botões de controle
        self.frame_botoes = tk.Frame(self.frame_lateral)
        self.frame_botoes.pack(pady=10)

        # Botões de controle
        self.botao_cor_aresta = tk.Button(self.frame_botoes, text="Mudar Cor da Aresta", command=self.mudar_cor_aresta)
        self.botao_cor_aresta.grid(row=0, column=0, padx=5, pady=5)

        self.botao_cor_preencher = tk.Button(self.frame_botoes, text="Mudar Cor de Preenchimento", command=self.mudar_cor_preencher)
        self.botao_cor_preencher.grid(row=1, column=0, padx=5, pady=5)

        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir", command=self.excluir_poligono)
        self.botao_excluir.grid(row=2, column=0, padx=5, pady=5)

        self.botao_limpar = tk.Button(self.frame_botoes, text="Limpar Tudo", command=self.limpar_canvas)
        self.botao_limpar.grid(row=3, column=0, padx=5, pady=5)

        self.botao_toggle_arestas = tk.Button(self.frame_botoes, text="Exibir Arestas", command=self.toggle_arestas)
        self.botao_toggle_arestas.grid(row=4, column=0, padx=5, pady=5)

        # Eventos de clique no canvas
        self.canvas.bind("<Button-1>", self.adicionar_ponto)
        self.canvas.bind("<Double-1>", self.fechar_poligono)

        # Frame para a lista de polígonos
        self.frame_poligonos = tk.Frame(self.frame_lateral)
        self.frame_poligonos.pack(fill=tk.Y)

    def toggle_arestas(self):
        """Alterna a exibição das arestas e atualiza o preenchimento se houver polígono selecionado."""
        self.exibir_arestas = not self.exibir_arestas
        texto = "Ocultar Arestas" if self.exibir_arestas else "Exibir Arestas"
        self.botao_toggle_arestas.config(text=texto)

        # Verifica se há um polígono selecionado antes de atualizar o preenchimento
        if self.poligono_selecionado is not None:
            if self.exibir_arestas:
                self.canvas.itemconfig(self.poligono_selecionado, outline=self.cor_aresta)
            else:
                self.canvas.itemconfig(self.poligono_selecionado, outline="")
            # Atualiza o preenchimento do polígono
            self.atualizar_preenchimento(self.poligono_selecionado)



    def adicionar_ponto(self, event):
        x, y = event.x, event.y
        self.pontos.append((x, y))
        raio = 2
        ponto_id = self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill='black')
        self.pontos_ids.append(ponto_id)

    def fechar_poligono(self, event):
        if len(self.pontos) > 2:
            poligono_id = self.canvas.create_polygon(self.pontos, outline=self.cor_aresta, fill='', width=2)
            self.poligonos.append(poligono_id)

            # Armazena pontos e IDs dos pontos associados ao polígono
            self.dados_poligonos[poligono_id] = {
                "pontos": list(self.pontos),
                "pontos_ids": list(self.pontos_ids)
            }

            self.preencher_poligono(self.pontos, poligono_id)
            self.pontos.clear()
            self.pontos_ids.clear()
            self.contador_poligonos += 1

            nome_poligono = f"Polígono {self.contador_poligonos}"
            botao_poligono = tk.Button(self.frame_poligonos, text=nome_poligono,
                                       command=lambda pid=poligono_id: self.selecionar_por_botao(pid))
            botao_poligono.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
            self.botao_poligonos[poligono_id] = botao_poligono

    def preencher_poligono(self, pontos, poligono_id):
        y_min = min(p[1] for p in pontos)
        y_max = max(p[1] for p in pontos)
        intersecoes = {y: [] for y in range(y_min, y_max + 1)}

        num_pontos = len(pontos)
        for i in range(num_pontos):
            x1, y1 = pontos[i]
            x2, y2 = pontos[(i + 1) % num_pontos]
            if y1 != y2:
                if y1 > y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1

                dx = x2 - x1
                dy = y2 - y1
                Tx = dx / dy

                x = x1
                for y in range(y1, y2):
                    intersecoes[y].append(x)
                    x += Tx

        self.linhas_preenchimento[poligono_id] = []
        for y, pontos_x in intersecoes.items():
            pontos_x.sort()
            for i in range(0, len(pontos_x) - 1, 2):
                x_ini = round(pontos_x[i])
                x_fim = round(pontos_x[i + 1])
                linha_id = self.canvas.create_line(x_ini, y, x_fim, y, fill=self.cor_preencher)
                self.linhas_preenchimento[poligono_id].append(linha_id)

    def selecionar_por_botao(self, poligono_id):
        self.poligono_selecionado = poligono_id
        for poligono in self.poligonos:
            if poligono == poligono_id:
                self.canvas.itemconfig(poligono, outline='red')
            else:
                self.canvas.itemconfig(poligono, outline=self.cor_aresta)
        self.canvas.itemconfig(poligono_id, outline='red')

    def mudar_cor_preencher(self):
        if self.poligono_selecionado:
            nova_cor = colorchooser.askcolor(title="Escolher Cor de Preenchimento")[1]
            if nova_cor:
                self.cor_preencher = nova_cor
                self.atualizar_preenchimento(self.poligono_selecionado)

    def atualizar_preenchimento(self, poligono_id):
        """Atualiza o preenchimento do polígono se ele existir."""
        if poligono_id in self.dados_poligonos:
            # Remove linhas antigas
            for linha_id in self.linhas_preenchimento.get(poligono_id, []):
                self.canvas.delete(linha_id)

            # Preenche novamente
            pontos = self.dados_poligonos[poligono_id]["pontos"]
            self.preencher_poligono(pontos, poligono_id)


    def mudar_cor_aresta(self):
        nova_cor = colorchooser.askcolor(title="Escolher Cor da Aresta")[1]
        if nova_cor:
            self.cor_aresta = nova_cor

    def excluir_poligono(self):
        if self.poligono_selecionado:
            dados = self.dados_poligonos.pop(self.poligono_selecionado, None)
            if dados:
                for ponto_id in dados["pontos_ids"]:
                    self.canvas.delete(ponto_id)
                for linha_id in self.linhas_preenchimento.get(self.poligono_selecionado, []):
                    self.canvas.delete(linha_id)

            self.canvas.delete(self.poligono_selecionado)
            self.poligonos.remove(self.poligono_selecionado)
            

            botao = self.botao_poligonos.pop(self.poligono_selecionado, None)
            if botao:
                botao.destroy()

            self.poligono_selecionado = None

    def limpar_canvas(self):
        self.canvas.delete("all")
        self.pontos.clear()
        self.pontos_ids.clear()
        self.poligonos.clear()
        self.poligono_selecionado = None
        for botao in self.botao_poligonos.values():
            botao.destroy()
        self.botao_poligonos.clear

if __name__ == "__main__":
    root = tk.Tk()
    app = PoligonoApp(root)

    root.mainloop()
