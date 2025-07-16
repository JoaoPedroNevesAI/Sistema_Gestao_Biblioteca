Sistema de Gestão de Biblioteca

Esse projeto foi feito para um trabalho de Estruturas de Dados, com o objetivo de organizar e listar dados de livros e usuários num sistema de gestão de biblioteca.

Funcionalidades:

-Cadastro de livros com título, autor, gênero e número de cópias
-Cadastro de usuários com nome e email
-Empréstimo de livros (com controle de disponibilidade)
-Reserva de livros (com fila de espera)
-Histórico de empréstimos de cada usuário (armazenado em lista encadeada)
-Ranking dos livros mais populares baseado nos empréstimos (implementado com heap)

Descrição do problema resolvido

Este projeto tem como objetivo resolver o problema de gerenciamento de uma biblioteca de forma simples e funcional. O sistema permite:

- Cadastro de usuários e livros;
- Empréstimos e devoluções de livros;
- Registro de histórico completo das atividades;
- Controle de acervo da biblioteca;
- Ranking de livros mais populares.

O sistema armazena os dados em arquivos `.csv`, garantindo persistência mesmo após o fechamento do programa.

---

Justificativa da escolha do tema

- O tema foi escolhido por ser prático e comum em ambientes acadêmicos e escolares. Portanto, um ótimo cenário para aplicar conceitos de estruturas de dados.

---

Estruturas de dados utilizadas e justificativas

 1. Dicionário:
- Permite acesso rápido e eficiente aos dados por chave.

 2. Lista:
- Fácil de manipular, percorrer e remover pares. Nesse projeto sendo os empréstimos de livros.

 3. Arquivos CSV:
- Simples e portável — ideal para projetos pequenos que não exigem bancos de dados complexos.

4. Heap:
- Permite um sistema de ordenação prática para encontrar os livros mais populares.

---

Desafios enfrentados e soluções encontradas

Leitura de arquivos:
- Problema: Ao tentar ler o cabeçalho como dado, causava erro de conversão.
- Solução: Adição de `next(f)` para pular o cabeçalho antes da leitura das linhas.

Persistência dos dados entre execuções:
- Problema: Os dados eram perdidos ao encerrar o sistema.
- Solução: Implementação de arquivos `.csv` para leitura e escrita.

Histórico de empréstimos incompleto:
- Problema: O histórico só mostrava livros emprestados, não devolvidos.
- Solução: Registro detalhado de ações ("emprestou" / "devolveu") com data/hora no `historico_emprestimos.csv`.

Reuso do sistema em diferentes máquinas:
- Problema: Dúvida se os dados seriam mantidos.
- Solução: Como os dados estão em arquivos `.csv`, basta copiar a pasta para manter tudo funcionando.

---

Instruções para executar o projeto

 1. Pré-requisitos:
- Ter o **Python 3.x** instalado.
- Ter o **VS Code** ou outro editor de código.
- Clonar o repositório ou copiar a pasta do projeto. (https://github.com/SEU_USUARIO/Sistema_Gestao_Biblioteca.git)

 2. No terminal: 
- Entre no arquivo: cd sistema-biblioteca

 3. Dentro da pasta: 
- Execute o programa: python main.py


---

##Como usar:

1. Clone este repositório no terminal:
git clone https://github.com/SEU_USUARIO/sistema-biblioteca.git

2. Entre no arquivo:
cd sistema-biblioteca

3. Execute o programa:
python main.py

Obrigado pela sua atenção :)
