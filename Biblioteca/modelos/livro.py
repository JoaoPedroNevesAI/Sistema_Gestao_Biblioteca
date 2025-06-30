class Livro:
    def __init__(self, id_livro, titulo, autor, genero, copias_disponiveis):
        # Identificador único do livro
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.copias_disponiveis = copias_disponiveis
        # Fila de IDs de usuários que reservaram esse livro
        self.fila_reservas = []

    def esta_disponivel(self):
        # Retorna True se houver cópias disponíveis
        return self.copias_disponiveis > 0

    def emprestar(self):
        # Tenta emprestar uma cópia, diminuindo o estoque
        if self.esta_disponivel():
            self.copias_disponiveis -= 1
            return True
        return False

    def devolver(self):
        # Devolve uma cópia, aumentando o estoque
        self.copias_disponiveis += 1

    def adicionar_reserva(self, id_usuario):
        # Adiciona um usuário à fila de reserva do livro
        self.fila_reservas.append(id_usuario)

    def proxima_reserva(self):
        # Retorna o próximo usuário da fila de reserva ou None se fila vazia
        if self.fila_reservas:
            return self.fila_reservas.pop(0)
        return None
