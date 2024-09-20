# Exercício 1: Gerenciamento de Livraria
# Você foi contratado para criar um sistema simples de gerenciamento de uma livraria.
# O sistema deve armazenar informações sobre livros e realizar operações CRUD para adicionar, visualizar,
# atualizar e remover livros da base de dados.

# Requisitos:
# Criar um banco de dados chamado livraria.db.
# Criar uma tabela livros com as seguintes colunas:
# id: chave primária, gerada automaticamente.
# titulo: texto, obrigatório.
# autor: texto, obrigatório.
# ano_publicacao: inteiro, obrigatório.
# preco: número de ponto flutuante, obrigatório.
# Funções CRUD:
# Função para adicionar um novo livro.
# Função para exibir todos os livros no banco de dados.
# Função para atualizar o preço de um livro baseado no título.
# Função para remover um livro baseado no título.
# Exemplo de Execução:
# Ao rodar o programa, você deve exibir um menu de opções como:

# Copiar código
# 1. Adicionar novo livro
# 2. Exibir todos os livros
# 3. Atualizar preço de um livro
# 4. Remover um livro
# 5. Sair

# O usuário poderá escolher uma opção e a operação correspondente será realizada.

# Desafio Extra:
# Adicionar uma função para **buscar
# um livro por autor**. A função deverá exibir todos os livros de um autor específico quando o usuário inserir o nome dele.



import sqlite3

# Função para criar a tabela 'livros'
def criar_tabela():
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para adicionar um novo livro
def adicionar_livro(titulo, autor, ano_publicacao, preco):
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))
    conexao.commit()
    conexao.close()

# Função para exibir todos os livros
def exibir_livros():
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    for livro in livros:
        print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: {livro[4]}")
    conexao.close()

# Função para atualizar o preço de um livro
def atualizar_preco(titulo, novo_preco):
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE livros SET preco = ? WHERE titulo = ?
    ''', (novo_preco, titulo))
    conexao.commit()
    conexao.close()

# Função para remover um livro
def remover_livro(titulo):
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()
    cursor.execute('''
        DELETE FROM livros WHERE titulo = ?
    ''', (titulo,))
    conexao.commit()
    conexao.close()

# Menu principal
def menu():
    criar_tabela()
    while True:
        print("\n1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano_publicacao = int(input("Ano de publicação: "))
            preco = float(input("Preço: "))
            adicionar_livro(titulo, autor, ano_publicacao, preco)
        elif opcao == '2':
            exibir_livros()
        elif opcao == '3':
            titulo = input("Título do livro para atualizar o preço: ")
            novo_preco = float(input("Novo preço: "))
            atualizar_preco(titulo, novo_preco)
        elif opcao == '4':
            titulo = input("Título do livro para remover: ")
            remover_livro(titulo)
        elif opcao == '5':
            break
        else:
            print("Opção inválida!")

# Executar o menu
menu()
