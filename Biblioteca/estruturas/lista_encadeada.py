class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

# Implementação simples de lista encadeada para armazenar histórico de empréstimos
class ListaEncadeada:
    def __init__(self):
        self.cabeca = None  # Início da lista

    def adicionar(self, dado):
        # Adiciona um dado no final da lista encadeada
        novo_no = No(dado)
        if not self.cabeca:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def listar(self):
        # Retorna uma lista com todos os dados armazenados na lista encadeada
        dados = []
        atual = self.cabeca
        while atual:
            dados.append(atual.dado)
            atual = atual.proximo
        return dados
