class Fila:
    def __init__(self):
        self.itens = []

    def enfileirar(self, item):
        # Adiciona item ao final da fila
        self.itens.append(item)

    def desenfileirar(self):
        # Remove e retorna o primeiro item da fila, ou None se vazia
        if self.esta_vazia():
            return None
        return self.itens.pop(0)

    def esta_vazia(self):
        # Verifica se a fila está vazia
        return len(self.itens) == 0

    def tamanho(self):
        # Retorna o número de itens na fila
        return len(self.itens)
