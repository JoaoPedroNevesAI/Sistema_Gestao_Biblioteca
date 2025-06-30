from modelos.livro import Livro
from modelos.usuario import Usuario
from estruturas.heap import HeapPopularidade

# Classe principal que gerencia toda a biblioteca
class SistemaBiblioteca:
    def __init__(self):
        self.livros = {}   # dicionário id_livro -> Livro
        self.usuarios = {} # dicionário id_usuario -> Usuario
        self.ranking = HeapPopularidade()

    def cadastrar_livro(self, id_livro, titulo, autor, genero, copias):
        if id_livro in self.livros:
            print(f"Erro: O ID '{id_livro}' já está cadastrado para outro livro.")
            return
        self.livros[id_livro] = Livro(id_livro, titulo, autor, genero, copias)
        print(f"Livro '{titulo}' cadastrado com sucesso.")

    def cadastrar_usuario(self, id_usuario, nome, email):
        if id_usuario in self.usuarios:
            print(f"Erro: O ID '{id_usuario}' já está cadastrado para outro usuário.")
            return
        self.usuarios[id_usuario] = Usuario(id_usuario, nome, email)
        print(f"Usuário '{nome}' cadastrado com sucesso.")

    def emprestar_livro(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return
        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return

        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]

        if livro.esta_disponivel():
            livro.emprestar()
            usuario.adicionar_ao_historico(livro)
            self.ranking.registrar_emprestimo(id_livro, livro.titulo)
            print(f"Livro '{livro.titulo}' emprestado para {usuario.nome}.")
        else:
            print(f"Livro indisponível. Usuário {usuario.nome} foi adicionado à fila de reserva.")
            livro.adicionar_reserva(id_usuario)

    def devolver_livro(self, id_livro):
        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return
        livro = self.livros[id_livro]
        livro.devolver()
        proximo = livro.proxima_reserva()
        if proximo:
            print(f"Notifique o usuário {proximo} que o livro '{livro.titulo}' está disponível.")
        else:
            print(f"Livro '{livro.titulo}' devolvido com sucesso.")

    def exibir_historico_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return
        historico = self.usuarios[id_usuario].ver_historico()
        print(f"Histórico de empréstimos do usuário {self.usuarios[id_usuario].nome}:")
        for item in historico:
            print(f"- {item['titulo']}")

    def exibir_ranking(self, top_n=5):
        ranking = self.ranking.ranking(top_n)
        print(f"\nTop {top_n} livros mais populares:")
        for i, (titulo, qtd) in enumerate(ranking, 1):
            print(f"{i}. {titulo} - {qtd} empréstimos")
