import heapq

class HeapPopularidade:
    def __init__(self):
        # Dicionário que armazena título e quantidade de empréstimos por livro
        self.contagem = {}  # id_livro -> (titulo, qtd)
        # Heap de tuplas (-qtd, id_livro, titulo) para criar max-heap via heapq
        self.heap = []

    def registrar_emprestimo(self, id_livro, titulo):
        # Atualiza contagem e adiciona no heap para manter ranking
        if id_livro in self.contagem:
            qtd = self.contagem[id_livro][1] + 1
        else:
            qtd = 1
        self.contagem[id_livro] = (titulo, qtd)
        heapq.heappush(self.heap, (-qtd, id_livro, titulo))

    def ranking(self, top_n=5):
        # Retorna os top N livros mais emprestados
        temp = []
        vistos = set()
        resultado = []

        while self.heap and len(resultado) < top_n:
            qtd_neg, id_livro, titulo = heapq.heappop(self.heap)
            qtd = -qtd_neg
            # Evita duplicatas e garante que pega o valor mais recente
            if id_livro in vistos:
                continue
            if self.contagem.get(id_livro, (None, 0))[1] == qtd:
                resultado.append((titulo, qtd))
                vistos.add(id_livro)
            else:
                continue
            temp.append((qtd_neg, id_livro, titulo))

        # Reinsere os itens processados para manter o heap intacto
        for item in temp:
            heapq.heappush(self.heap, item)

        return resultado
