from estruturas.lista_encadeada import ListaEncadeada

class Usuario:
    def __init__(self, id_usuario, nome, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        # Histórico de empréstimos do usuário armazenado em lista encadeada
        self.historico_emprestimos = ListaEncadeada()

    def adicionar_ao_historico(self, livro):
        # Adiciona um livro ao histórico do usuário
        self.historico_emprestimos.adicionar({
            "id_livro": livro.id_livro,
            "titulo": livro.titulo
        })

    def ver_historico(self):
        # Retorna a lista de empréstimos do usuário
        return self.historico_emprestimos.listar()
