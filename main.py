from sistema.sistema import SistemaBiblioteca

sistema = SistemaBiblioteca()


def menu():
    print("\n========== SISTEMA DE GESTÃO DE BIBLIOTECA ==========")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Emprestar livro")
    print("4. Devolver livro")
    print("5. Ver empréstimos ativos do usuário")
    print("6. Ver histórico completo do usuário")
    print("7. Listar acervo da biblioteca")
    print("8. Exibir ranking de popularidade")
    print("9. Ver fila de reservas")
    print("10. Relatório geral")
    print("11. Remover usuário")
    print("12. Remover livro")
    print("0. Sair")


def ler_id(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor.isdigit():
            return valor

        print("Digite apenas números.")


def ler_nome(mensagem):
    while True:
        valor = input(mensagem).strip()

        if not valor:
            print("Campo obrigatório.")
            continue

        valido = True

        for c in valor:
            if not (c.isalpha() or c in " .-'"):
                valido = False
                break

        if valido:
            return valor

        print("Digite apenas letras.")


def ler_email():
    while True:
        valor = input("Email: ").strip()

        if "@" in valor and "." in valor:
            return valor

        print("Email inválido.")


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("Campo obrigatório.")


def ler_numero(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor.isdigit() and int(valor) > 0:
            return int(valor)

        print("Digite apenas números inteiros maiores que zero.")


while True:
    menu()
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        while True:
            id_livro = ler_id("ID do livro: ")

            if id_livro not in sistema.livros:
                break

            print("Já existe um livro com esse ID.")

        titulo = ler_texto("Título: ")
        autor = ler_nome("Autor: ")
        genero = ler_nome("Gênero: ")
        copias = ler_numero("Número de cópias: ")

        sistema.cadastrar_livro(id_livro, titulo, autor, genero, copias)

    elif opcao == "2":
        while True:
            id_usuario = ler_id("ID do usuário: ")

            if id_usuario not in sistema.usuarios:
                break

            print("Já existe um usuário com esse ID.")

        nome = ler_nome("Nome: ")
        email = ler_email()

        sistema.cadastrar_usuario(id_usuario, nome, email)

    elif opcao == "3":
        id_usuario = ler_id("ID do usuário: ")
        id_livro = ler_id("ID do livro: ")

        sistema.emprestar_livro(id_usuario, id_livro)

    elif opcao == "4":
        id_usuario = ler_id("ID do usuário: ")
        id_livro = ler_id("ID do livro: ")

        sistema.devolver_livro(id_usuario, id_livro)

    elif opcao == "5":
        id_usuario = ler_id("ID do usuário: ")

        sistema.exibir_historico_usuario(id_usuario)

    elif opcao == "6":
        id_usuario = ler_id("ID do usuário: ")

        sistema.exibir_historico_completo(id_usuario)

    elif opcao == "7":
        sistema.listar_acervo()

    elif opcao == "8":
        sistema.exibir_ranking_popularidade()

    elif opcao == "9":
        sistema.exibir_filas_reserva()

    elif opcao == "10":
        sistema.relatorio_geral()

    elif opcao == "11":
        id_usuario = ler_id("ID do usuário: ")
        sistema.remover_usuario(id_usuario)

    elif opcao == "12":
        id_livro = ler_id("ID do livro: ")
        sistema.remover_livro(id_livro)

    elif opcao == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida.")