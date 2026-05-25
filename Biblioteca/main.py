from sistema.sistema import SistemaBiblioteca

sistema = SistemaBiblioteca()

def menu():
    print("\n--- SISTEMA DE GESTÃO DE BIBLIOTECA ---")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Emprestar livro")
    print("4. Devolver livro")
    print("5. Ver empréstimos ativos do usuário")
    print("6. Ver histórico completo do usuário")
    print("7. Listar acervo da biblioteca")
    print("8. Exibir ranking de popularidade dos livros")
    print("0. Sair")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        id_livro = input("ID do livro: ")
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Gênero: ")
        try:
            copias = int(input("Número de cópias: "))
        except ValueError:
            print("Número de cópias inválido. Tente novamente.")
            continue
        sistema.cadastrar_livro(id_livro, titulo, autor, genero, copias)

    elif opcao == "2":
        id_usuario = input("ID do usuário: ")
        nome = input("Nome: ")
        email = input("Email: ")
        sistema.cadastrar_usuario(id_usuario, nome, email)

    elif opcao == "3":
        id_usuario = input("ID do usuário: ")
        id_livro = input("ID do livro: ")
        sistema.emprestar_livro(id_usuario, id_livro)

    elif opcao == "4":
        id_usuario = input("ID do usuário: ")
        id_livro = input("ID do livro: ")
        sistema.devolver_livro(id_usuario, id_livro)

    elif opcao == "5":
        id_usuario = input("ID do usuário: ")
        sistema.exibir_historico_usuario(id_usuario)

    elif opcao == "6":
        id_usuario = input("ID do usuário: ")
        sistema.exibir_historico_completo(id_usuario)

    elif opcao == "7":
        sistema.listar_acervo()

    elif opcao == "8":
        sistema.exibir_ranking_popularidade()

    elif opcao == "0":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")
