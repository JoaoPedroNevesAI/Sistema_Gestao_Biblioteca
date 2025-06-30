from sistema.sistema import SistemaBiblioteca

sistema = SistemaBiblioteca()

def menu():
    print("\n--- SISTEMA DE GESTÃO DE BIBLIOTECA ---")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Emprestar livro")
    print("4. Devolver livro")
    print("5. Ver histórico do usuário")
    print("6. Ver ranking de popularidade")
    print("0. Sair")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        id_livro = input("ID do livro: ")
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Gênero: ")
        copias = int(input("Número de cópias: "))
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
        id_livro = input("ID do livro: ")
        sistema.devolver_livro(id_livro)

    elif opcao == "5":
        id_usuario = input("ID do usuário: ")
        sistema.exibir_historico_usuario(id_usuario)

    elif opcao == "6":
        sistema.exibir_ranking()

    elif opcao == "0":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida.")
