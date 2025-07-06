import os
import datetime
from modelos.usuario import Usuario
from modelos.livro import Livro

# Caminhos dos arquivos CSV
USUARIOS_CSV = "usuarios.csv"
LIVROS_CSV = "livros.csv"
EMPRESTIMOS_CSV = "emprestimos.csv"
HISTORICO_CSV = "historico_emprestimos.csv"  # <== variável definida corretamente

class SistemaBiblioteca:
    def __init__(self):
        self.usuarios = {}    # id_usuario -> Usuario
        self.livros = {}      # id_livro -> Livro
        self.emprestimos = [] # lista de (id_usuario, id_livro)

        # Cria os arquivos CSV se não existirem
        self._criar_arquivos_csv()

        # Carrega os dados dos CSVs
        self.carregar_usuarios()
        self.carregar_livros()
        self.carregar_emprestimos()

    def _criar_arquivos_csv(self):
        for arquivo in [USUARIOS_CSV, LIVROS_CSV, EMPRESTIMOS_CSV, HISTORICO_CSV]:
            if not os.path.exists(arquivo):
                with open(arquivo, "w") as f:
                    # Se for o arquivo histórico, já escreve o cabeçalho
                    if arquivo == HISTORICO_CSV:
                        f.write("id_usuario,id_livro,acao,data_hora\n")

    # --- Usuários ---
    def carregar_usuarios(self):
        if not os.path.exists(USUARIOS_CSV):
            return
        with open(USUARIOS_CSV, "r") as f:
            next(f)  # Pula o cabeçalho
            for linha in f:
                usuario = Usuario.from_csv(linha)
                if usuario:
                    self.usuarios[usuario.id_usuario] = usuario

    def salvar_usuarios(self):
        with open(USUARIOS_CSV, "w") as f:
            for usuario in self.usuarios.values():
                f.write(usuario.to_csv())

    def cadastrar_usuario(self, id_usuario, nome, email):
        if id_usuario in self.usuarios:
            print("Erro: ID de usuário já existe.")
            return False
        usuario = Usuario(id_usuario, nome, email)
        self.usuarios[id_usuario] = usuario
        self.salvar_usuarios()
        print("Usuário cadastrado com sucesso!")
        return True

    # --- Livros ---
    def carregar_livros(self):
        if not os.path.exists(LIVROS_CSV):
            return
        with open(LIVROS_CSV, "r") as f:
            next(f)  # Pula a linha do cabeçalho
            for linha in f:
                livro = Livro.from_csv(linha)
                if livro:
                    self.livros[livro.id_livro] = livro


    def salvar_livros(self):
        with open(LIVROS_CSV, "w") as f:
            for livro in self.livros.values():
                f.write(livro.to_csv())

    def cadastrar_livro(self, id_livro, titulo, autor, genero, copias):
        if id_livro in self.livros:
            print("Erro: ID de livro já existe.")
            return False
        livro = Livro(id_livro, titulo, autor, genero, copias)
        self.livros[id_livro] = livro
        self.salvar_livros()
        print("Livro cadastrado com sucesso!")
        return True

    # --- Empréstimos ---
    def carregar_emprestimos(self):
        if not os.path.exists(EMPRESTIMOS_CSV):
            return
        with open(EMPRESTIMOS_CSV, "r") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    self.emprestimos.append( (partes[0], partes[1]) )

    def salvar_emprestimos(self):
        with open(EMPRESTIMOS_CSV, "w") as f:
            for emp in self.emprestimos:
                f.write(f"{emp[0]},{emp[1]}\n")

    # Função para registrar histórico de empréstimos e devoluções
    def registrar_historico(self, id_usuario, id_livro, acao):
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORICO_CSV, "a") as f:
            f.write(f"{id_usuario},{id_livro},{acao},{data_hora}\n")

    def emprestar_livro(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return False
        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return False
        livro = self.livros[id_livro]
        if livro.copias < 1:
            print("Não há cópias disponíveis.")
            return False

        livro.copias -= 1
        self.emprestimos.append( (id_usuario, id_livro) )
        self.salvar_livros()
        self.salvar_emprestimos()
        self.registrar_historico(id_usuario, id_livro, "emprestou")
        print(f"Livro '{livro.titulo}' emprestado para usuário {self.usuarios[id_usuario].nome}")
        return True

    def devolver_livro(self, id_usuario, id_livro):
        if (id_usuario, id_livro) not in self.emprestimos:
            print("Empréstimo não encontrado.")
            return False
        livro = self.livros.get(id_livro)
        if not livro:
            print("Livro não encontrado.")
            return False

        livro.copias += 1
        self.emprestimos.remove( (id_usuario, id_livro) )
        self.salvar_livros()
        self.salvar_emprestimos()
        self.registrar_historico(id_usuario, id_livro, "devolveu")
        print(f"Livro '{livro.titulo}' devolvido pelo usuário {self.usuarios[id_usuario].nome}")
        return True

    # Exibir histórico completo (empréstimos e devoluções) do usuário
    def exibir_historico_completo(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return
        print(f"\nHistórico completo do usuário {self.usuarios[id_usuario].nome}:")
        if not os.path.exists(HISTORICO_CSV):
            print("Nenhum histórico registrado.")
            return
        with open(HISTORICO_CSV, "r") as f:
            next(f)  # pular cabeçalho
            linhas = f.readlines()
        historico_usuario = [linha.strip() for linha in linhas if linha.startswith(id_usuario + ",")]
        if not historico_usuario:
            print("Nenhum registro encontrado.")
            return
        for linha in historico_usuario:
            _, id_livro, acao, data_hora = linha.split(",")
            livro = self.livros.get(id_livro)
            titulo = livro.titulo if livro else "Livro removido"
            print(f"{data_hora} - {acao.capitalize()} - {titulo} (ID: {id_livro})")

    # Exibir apenas empréstimos ativos do usuário
    def exibir_historico_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuário não encontrado.")
            return
        print(f"\nEmpréstimos ativos do usuário {self.usuarios[id_usuario].nome}:")
        encontrou = False
        for (user_id, livro_id) in self.emprestimos:
            if user_id == id_usuario:
                livro = self.livros.get(livro_id)
                titulo = livro.titulo if livro else "Livro removido"
                print(f"- {titulo} (ID: {livro_id})")
                encontrou = True
        if not encontrou:
            print("Nenhum empréstimo ativo encontrado.")

    # Listar todo o acervo da biblioteca
    def listar_acervo(self):
        if not self.livros:
            print("Não há livros cadastrados no acervo.")
            return
        print("\n--- Acervo da Biblioteca ---")
        for livro in self.livros.values():
            print(f"ID: {livro.id_livro} | Título: {livro.titulo} | Autor: {livro.autor} | Gênero: {livro.genero} | Cópias disponíveis: {livro.copias}")

    # Ranking de popularidade dos livros
    def exibir_ranking_popularidade(self):
        if not os.path.exists(HISTORICO_CSV):
            print("Nenhum histórico registrado.")
            return
        
        contagem = {}

        with open(HISTORICO_CSV, "r") as f:
            next(f)  # pula cabeçalho
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) < 4:
                    continue
                _, id_livro, acao, _ = partes
                if acao == "emprestou":
                    contagem[id_livro] = contagem.get(id_livro, 0) + 1

        if not contagem:
            print("Nenhum empréstimo registrado.")
            return

        ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

        print("\n--- Ranking de Popularidade dos Livros ---")
        for i, (id_livro, qtd) in enumerate(ranking, start=1):
            livro = self.livros.get(id_livro)
            titulo = livro.titulo if livro else "Livro removido"
            print(f"{i}. {titulo} (ID: {id_livro}) - {qtd} empréstimos")
