import os
import datetime

from modelos.usuario import Usuario
from modelos.livro import Livro

from estruturas.fila import Fila
from estruturas.heap import HeapPopularidade
from estruturas.lista_encadeada import ListaEncadeada


PASTA_DADOS = "dados"

USUARIOS_CSV = f"{PASTA_DADOS}/usuarios.csv"
LIVROS_CSV = f"{PASTA_DADOS}/livros.csv"
EMPRESTIMOS_CSV = f"{PASTA_DADOS}/emprestimos.csv"
HISTORICO_CSV = f"{PASTA_DADOS}/historico_emprestimos.csv"


class SistemaBiblioteca:
    def __init__(self):
        self.usuarios = {}
        self.livros = {}
        self.emprestimos = []

        self.reservas = {}

        self.popularidade = HeapPopularidade()
        self.historico = ListaEncadeada()

        self.ids_usuarios_removidos = set()
        self.ids_livros_removidos = set()

        self._criar_arquivos_csv()

        self.carregar_usuarios()
        self.carregar_livros()
        self.carregar_emprestimos()
        self.carregar_historico()

    def sucesso(self, mensagem):
        print("\n" + "=" * 50)
        print(f"✅ {mensagem}".center(50))
        print("=" * 50)

    def erro(self, mensagem):
        print("\n" + "=" * 50)
        print(f"❌ {mensagem}".center(50))
        print("=" * 50)

    def aviso(self, mensagem):
        print("\n" + "=" * 50)
        print(f"⚠️ {mensagem}".center(50))
        print("=" * 50)

    def _criar_arquivos_csv(self):
        if not os.path.exists(PASTA_DADOS):
            os.makedirs(PASTA_DADOS)

        if not os.path.exists(USUARIOS_CSV):
            with open(USUARIOS_CSV, "w", encoding="utf-8") as f:
                f.write("id,nome,email\n")

        if not os.path.exists(LIVROS_CSV):
            with open(LIVROS_CSV, "w", encoding="utf-8") as f:
                f.write("id,titulo,autor,genero,copias\n")

        if not os.path.exists(EMPRESTIMOS_CSV):
            open(EMPRESTIMOS_CSV, "w", encoding="utf-8").close()

        if not os.path.exists(HISTORICO_CSV):
            with open(HISTORICO_CSV, "w", encoding="utf-8") as f:
                f.write("id_usuario,id_livro,acao,data_hora\n")

    def carregar_usuarios(self):
        with open(USUARIOS_CSV, "r", encoding="utf-8") as f:
            linhas = f.readlines()

            if len(linhas) <= 1:
                return

            for linha in linhas[1:]:
                usuario = Usuario.from_csv(linha)

                if usuario:
                    self.usuarios[usuario.id_usuario] = usuario

    def salvar_usuarios(self):
        with open(USUARIOS_CSV, "w", encoding="utf-8") as f:
            f.write("id,nome,email\n")

            for usuario in self.usuarios.values():
                f.write(usuario.to_csv())

    def carregar_livros(self):
        with open(LIVROS_CSV, "r", encoding="utf-8") as f:
            linhas = f.readlines()

            if len(linhas) <= 1:
                return

            for linha in linhas[1:]:
                livro = Livro.from_csv(linha)

                if livro:
                    self.livros[livro.id_livro] = livro

    def salvar_livros(self):
        with open(LIVROS_CSV, "w", encoding="utf-8") as f:
            f.write("id,titulo,autor,genero,copias\n")

            for livro in self.livros.values():
                f.write(livro.to_csv())

    def carregar_emprestimos(self):
        with open(EMPRESTIMOS_CSV, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(",")

                if len(partes) == 2:
                    self.emprestimos.append((partes[0], partes[1]))

    def salvar_emprestimos(self):
        with open(EMPRESTIMOS_CSV, "w", encoding="utf-8") as f:
            for usuario, livro in self.emprestimos:
                f.write(f"{usuario},{livro}\n")

    def carregar_historico(self):
        with open(HISTORICO_CSV, "r", encoding="utf-8") as f:
            linhas = f.readlines()

            if len(linhas) <= 1:
                return

            for linha in linhas[1:]:
                linha = linha.strip()

                if linha:
                    self.historico.adicionar(linha)

    def registrar_historico(self, id_usuario, id_livro, acao):
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        linha = f"{id_usuario},{id_livro},{acao},{data_hora}"

        self.historico.adicionar(linha)

        with open(HISTORICO_CSV, "a", encoding="utf-8") as f:
            f.write(linha + "\n")

    def cadastrar_usuario(self, id_usuario, nome, email):
        if not id_usuario.isdigit():
            self.erro("ID do usuário deve conter apenas números.")
            return False

        if id_usuario in self.usuarios:
            self.erro("Já existe um usuário com esse ID.")
            return False

        if id_usuario in self.ids_usuarios_removidos:
            self.erro("Esse ID já foi utilizado anteriormente.")
            return False

        self.usuarios[id_usuario] = Usuario(
            id_usuario,
            nome,
            email
        )

        self.salvar_usuarios()

        self.sucesso("Usuário cadastrado com sucesso.")
        return True

    def cadastrar_livro(self, id_livro, titulo, autor, genero, copias):
        if not id_livro.isdigit():
            self.erro("ID do livro deve conter apenas números.")
            return False

        if id_livro in self.livros:
            self.erro("Já existe um livro com esse ID.")
            return False

        if id_livro in self.ids_livros_removidos:
            self.erro("Esse ID já foi utilizado anteriormente.")
            return False

        self.livros[id_livro] = Livro(
            id_livro,
            titulo,
            autor,
            genero,
            copias
        )

        self.salvar_livros()

        self.sucesso("Livro cadastrado com sucesso.")
        return True

    def emprestar_livro(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            self.erro("Usuário não encontrado.")
            return False

        if id_livro not in self.livros:
            self.erro("Livro não encontrado.")
            return False

        livro = self.livros[id_livro]

        if livro.copias < 1:
            if id_livro not in self.reservas:
                self.reservas[id_livro] = Fila()

            self.reservas[id_livro].enfileirar(id_usuario)

            self.aviso("Sem cópias disponíveis. Usuário adicionado à fila.")
            return False

        livro.copias -= 1

        self.emprestimos.append((id_usuario, id_livro))

        self.popularidade.registrar_emprestimo(
            id_livro,
            livro.titulo
        )

        self.salvar_livros()
        self.salvar_emprestimos()

        self.registrar_historico(
            id_usuario,
            id_livro,
            "emprestou"
        )

        self.sucesso("Livro emprestado com sucesso.")
        return True

    def devolver_livro(self, id_usuario, id_livro):
        if (id_usuario, id_livro) not in self.emprestimos:
            self.erro("Empréstimo não encontrado.")
            return False

        livro = self.livros[id_livro]

        self.emprestimos.remove((id_usuario, id_livro))

        livro.copias += 1

        self.salvar_emprestimos()
        self.salvar_livros()

        self.registrar_historico(
            id_usuario,
            id_livro,
            "devolveu"
        )

        self.sucesso("Livro devolvido com sucesso.")
        return True

    def exibir_historico_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            self.erro("Usuário não encontrado.")
            return

        print("\nEMPRÉSTIMOS ATIVOS:")

        encontrou = False

        for usuario, livro_id in self.emprestimos:
            if usuario == id_usuario:
                livro = self.livros[livro_id]

                print(f"- {livro.titulo}")

                encontrou = True

        if not encontrou:
            self.aviso("Nenhum empréstimo ativo.")

    def exibir_historico_completo(self, id_usuario):
        if id_usuario not in self.usuarios:
            self.erro("Usuário não encontrado.")
            return

        print("\nHISTÓRICO COMPLETO:")

        encontrou = False

        for item in self.historico.listar():
            if item.startswith(id_usuario + ","):
                partes = item.split(",")

                _, id_livro, acao, data = partes

                titulo = self.livros[id_livro].titulo \
                    if id_livro in self.livros \
                    else "Livro removido"

                print(f"{data} - {acao} - {titulo}")

                encontrou = True

        if not encontrou:
            self.aviso("Nenhum registro encontrado.")

    def listar_acervo(self):
        if not self.livros:
            self.aviso("Nenhum livro cadastrado.")
            return

        print("\nACERVO:")

        for livro in self.livros.values():
            print(
                f"ID: {livro.id_livro} | "
                f"Título: {livro.titulo} | "
                f"Autor: {livro.autor} | "
                f"Gênero: {livro.genero} | "
                f"Cópias: {livro.copias}"
            )

    def exibir_ranking_popularidade(self):
        ranking = self.popularidade.ranking()

        if not ranking:
            self.aviso("Nenhum empréstimo registrado.")
            return

        print("\nRANKING DOS LIVROS:")

        for posicao, (titulo, qtd) in enumerate(ranking, start=1):
            print(f"{posicao}. {titulo} - {qtd} empréstimos")

    def exibir_filas_reserva(self):
        if not self.reservas:
            self.aviso("Não há reservas registradas.")
            return

        print("\nFILAS DE RESERVA:")

        encontrou = False

        for id_livro, fila in self.reservas.items():
            if fila.esta_vazia():
                continue

            encontrou = True

            livro = self.livros.get(id_livro)

            titulo = livro.titulo if livro else "Livro removido"

            print(f"\nLivro: {titulo}")

            for posicao, id_usuario in enumerate(fila.itens, start=1):
                usuario = self.usuarios.get(id_usuario)

                nome = usuario.nome if usuario else "Usuário removido"

                print(f"{posicao}. {nome}")

        if not encontrou:
            self.aviso("Não há reservas pendentes.")

    def relatorio_geral(self):
        total_usuarios = len(self.usuarios)
        total_livros = len(self.livros)
        emprestimos_ativos = len(self.emprestimos)

        reservas = 0

        for fila in self.reservas.values():
            reservas += fila.tamanho()

        ranking = self.popularidade.ranking(1)

        print("\nRELATÓRIO GERAL")
        print("-" * 40)

        print(f"Usuários cadastrados: {total_usuarios}")
        print(f"Livros cadastrados: {total_livros}")
        print(f"Empréstimos ativos: {emprestimos_ativos}")
        print(f"Reservas pendentes: {reservas}")

        if ranking:
            titulo, qtd = ranking[0]

            print(f"Livro mais popular: {titulo} ({qtd} empréstimos)")

    def remover_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            self.erro("Usuário não encontrado.")
            return False

        for usuario, _ in self.emprestimos:
            if usuario == id_usuario:
                self.erro("Usuário possui empréstimos ativos.")
                return False

        self.ids_usuarios_removidos.add(id_usuario)

        del self.usuarios[id_usuario]

        self.salvar_usuarios()

        self.sucesso("Usuário removido com sucesso.")
        return True

    def remover_livro(self, id_livro):
        if id_livro not in self.livros:
            self.erro("Livro não encontrado.")
            return False

        for _, livro in self.emprestimos:
            if livro == id_livro:
                self.erro("Livro está emprestado.")
                return False

        self.ids_livros_removidos.add(id_livro)

        del self.livros[id_livro]

        self.salvar_livros()

        self.sucesso("Livro removido com sucesso.")
        return True