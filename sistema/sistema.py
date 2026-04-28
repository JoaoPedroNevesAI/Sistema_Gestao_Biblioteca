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

        self._criar_arquivos_csv()

        self.carregar_usuarios()
        self.carregar_livros()
        self.carregar_emprestimos()
        self.carregar_historico()

    def _criar_arquivos_csv(self):
        if not os.path.exists(PASTA_DADOS):
            os.makedirs(PASTA_DADOS)

        if not os.path.exists(USUARIOS_CSV):
            with open(USUARIOS_CSV, "w") as f:
                f.write("id,nome,email\n")

        if not os.path.exists(LIVROS_CSV):
            with open(LIVROS_CSV, "w") as f:
                f.write("id,titulo,autor,genero,copias\n")

        if not os.path.exists(EMPRESTIMOS_CSV):
            open(EMPRESTIMOS_CSV, "w").close()

        if not os.path.exists(HISTORICO_CSV):
            with open(HISTORICO_CSV, "w") as f:
                f.write("id_usuario,id_livro,acao,data_hora\n")

    def carregar_usuarios(self):
        with open(USUARIOS_CSV, "r") as f:
            next(f)
            for linha in f:
                usuario = Usuario.from_csv(linha)
                if usuario:
                    self.usuarios[usuario.id_usuario] = usuario

    def salvar_usuarios(self):
        with open(USUARIOS_CSV, "w") as f:
            f.write("id,nome,email\n")
            for usuario in self.usuarios.values():
                f.write(usuario.to_csv())

    def carregar_livros(self):
        with open(LIVROS_CSV, "r") as f:
            next(f)
            for linha in f:
                livro = Livro.from_csv(linha)
                if livro:
                    self.livros[livro.id_livro] = livro

    def salvar_livros(self):
        with open(LIVROS_CSV, "w") as f:
            f.write("id,titulo,autor,genero,copias\n")
            for livro in self.livros.values():
                f.write(livro.to_csv())

    def carregar_emprestimos(self):
        with open(EMPRESTIMOS_CSV, "r") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    self.emprestimos.append((partes[0], partes[1]))

    def salvar_emprestimos(self):
        with open(EMPRESTIMOS_CSV, "w") as f:
            for usuario, livro in self.emprestimos:
                f.write(f"{usuario},{livro}\n")

    def carregar_historico(self):
        with open(HISTORICO_CSV, "r") as f:
            next(f)
            for linha in f:
                linha = linha.strip()
                if linha:
                    self.historico.adicionar(linha)

                    partes = linha.split(",")
                    if len(partes) == 4:
                        _, id_livro, acao, _ = partes

                        if acao == "emprestou" and id_livro in self.livros:
                            titulo = self.livros[id_livro].titulo
                            self.popularidade.registrar_emprestimo(id_livro, titulo)

    def cadastrar_usuario(self, id_usuario, nome, email):
        if not id_usuario.isdigit():
            print("ID do usuário deve conter apenas números.")
            return False

        if id_usuario in self.usuarios:
            print("Usuário já existe.")
            return False

        if not nome.replace(" ", "").isalpha():
            print("Nome deve conter apenas letras.")
            return False

        if "@" not in email or "." not in email:
            print("Email inválido.")
            return False

        self.usuarios[id_usuario] = Usuario(id_usuario, nome, email)
        self.salvar_usuarios()

        print("Usuário cadastrado com sucesso.")
        return True

    def cadastrar_livro(self, id_livro, titulo, autor, genero, copias):
        if not id_livro.isdigit():
            print("ID do livro deve conter apenas números.")
            return False

        if id_livro in self.livros:
            print("Livro já existe.")
            return False

        if not titulo.strip():
            print("Título inválido.")
            return False

        if not autor.replace(" ", "").isalpha():
            print("Autor deve conter apenas letras.")
            return False

        if not genero.replace(" ", "").isalpha():
            print("Gênero deve conter apenas letras.")
            return False

        if not isinstance(copias, int) or copias <= 0:
            print("Quantidade de cópias deve ser um número inteiro maior que zero.")
            return False

        self.livros[id_livro] = Livro(id_livro, titulo, autor, genero, copias)
        self.salvar_livros()

        print("Livro cadastrado com sucesso.")
        return True

    def registrar_historico(self, id_usuario, id_livro, acao):
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"{id_usuario},{id_livro},{acao},{data_hora}"

        self.historico.adicionar(linha)

        with open(HISTORICO_CSV, "a") as f:
            f.write(linha + "\n")

    def emprestar_livro(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return False

        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return False

        if (id_usuario, id_livro) in self.emprestimos:
            print("Usuário já possui este livro.")
            return False

        livro = self.livros[id_livro]

        if livro.copias < 1:
            if id_livro not in self.reservas:
                self.reservas[id_livro] = Fila()

            self.reservas[id_livro].enfileirar(id_usuario)

            print("Sem cópias disponíveis. Usuário adicionado à fila de reserva.")
            return False

        livro.copias -= 1
        self.emprestimos.append((id_usuario, id_livro))

        self.popularidade.registrar_emprestimo(id_livro, livro.titulo)

        self.salvar_livros()
        self.salvar_emprestimos()
        self.registrar_historico(id_usuario, id_livro, "emprestou")

        print("Livro emprestado com sucesso.")
        return True

    def devolver_livro(self, id_usuario, id_livro):
        if (id_usuario, id_livro) not in self.emprestimos:
            print("Empréstimo não encontrado.")
            return False

        livro = self.livros[id_livro]

        self.emprestimos.remove((id_usuario, id_livro))
        livro.copias += 1

        self.salvar_emprestimos()
        self.salvar_livros()
        self.registrar_historico(id_usuario, id_livro, "devolveu")

        if id_livro in self.reservas:
            fila = self.reservas[id_livro]

            if not fila.esta_vazia():
                proximo_usuario = fila.desenfileirar()

                livro.copias -= 1
                self.emprestimos.append((proximo_usuario, id_livro))

                self.popularidade.registrar_emprestimo(id_livro, livro.titulo)

                self.salvar_emprestimos()
                self.salvar_livros()
                self.registrar_historico(proximo_usuario, id_livro, "emprestou")

                print("Livro reservado entregue automaticamente.")

        print("Livro devolvido com sucesso.")
        return True

    def exibir_historico_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return

        print("\nEmpréstimos ativos:")

        encontrou = False

        for usuario, livro_id in self.emprestimos:
            if usuario == id_usuario:
                livro = self.livros[livro_id]
                print(f"- {livro.titulo}")
                encontrou = True

        if not encontrou:
            print("Nenhum empréstimo ativo.")

    def exibir_historico_completo(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return

        print("\nHistórico completo:")

        dados = self.historico.listar()
        encontrou = False

        for item in dados:
            if item.startswith(id_usuario + ","):
                partes = item.split(",")

                _, id_livro, acao, data = partes

                titulo = self.livros[id_livro].titulo if id_livro in self.livros else "Livro removido"

                print(f"{data} - {acao} - {titulo}")
                encontrou = True

        if not encontrou:
            print("Nenhum registro.")

    def listar_acervo(self):
        if not self.livros:
            print("Nenhum livro cadastrado.")
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
            print("Nenhum empréstimo registrado.")
            return

        print("\nRANKING DOS LIVROS:")

        for posicao, (titulo, qtd) in enumerate(ranking, start=1):
            print(f"{posicao}. {titulo} - {qtd} empréstimos")

    def exibir_filas_reserva(self):
        if not self.reservas:
            print("Não há reservas registradas.")
            return

        print("\n=== FILAS DE RESERVA ===")

        encontrou = False

        for id_livro, fila in self.reservas.items():
            if fila.esta_vazia():
                continue

            encontrou = True

            livro = self.livros.get(id_livro)
            titulo = livro.titulo if livro else "Livro removido"

            print(f"\nLivro: {titulo} (ID: {id_livro})")

            for posicao, id_usuario in enumerate(fila.itens, start=1):
                usuario = self.usuarios.get(id_usuario)
                nome = usuario.nome if usuario else "Usuário removido"

                print(f"{posicao}. {nome} (ID: {id_usuario})")

        if not encontrou:
            print("Não há reservas pendentes.")

    def relatorio_geral(self):
        total_usuarios = len(self.usuarios)
        total_livros = len(self.livros)
        emprestimos_ativos = len(self.emprestimos)

        reservas = 0
        for fila in self.reservas.values():
            reservas += fila.tamanho()

        ranking = self.popularidade.ranking(1)

        print("\n========== RELATÓRIO GERAL ==========")
        print(f"Usuários cadastrados: {total_usuarios}")
        print(f"Livros cadastrados: {total_livros}")
        print(f"Empréstimos ativos: {emprestimos_ativos}")
        print(f"Reservas pendentes: {reservas}")

        if ranking:
            titulo, qtd = ranking[0]
            print(f"Livro mais popular: {titulo} ({qtd} empréstimos)")
        else:
            print("Livro mais popular: Nenhum empréstimo registrado")

    def remover_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return False

        for usuario, _ in self.emprestimos:
            if usuario == id_usuario:
                print("Usuário possui empréstimos ativos.")
                return False

        for fila in self.reservas.values():
            if id_usuario in fila.itens:
                print("Usuário está em fila de reserva.")
                return False

        del self.usuarios[id_usuario]
        self.salvar_usuarios()

        print("Usuário removido com sucesso.")
        return True


    def remover_livro(self, id_livro):
        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return False

        for _, livro in self.emprestimos:
            if livro == id_livro:
                print("Livro está emprestado no momento.")
                return False

        if id_livro in self.reservas:
            if not self.reservas[id_livro].esta_vazia():
                print("Livro possui fila de reserva.")
                return False

        del self.livros[id_livro]
        self.salvar_livros()

        print("Livro removido com sucesso.")
        return True