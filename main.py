import sqlite3
from datetime import datetime 
import csv
import os

def iniciar_banco():
    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    connect.commit()
    connect.close()

def novo_livro():
    while True:
        titulo = input('Digite o título do livro: ')
        if not titulo.strip():  # Verifica se o título não está vazio
            print("Título não pode ser vazio. Tente novamente.")
            continue
        break

    while True:
        autor = input('Digite o autor do livro: ')
        if not autor.strip():  # Verifica se o autor não está vazio
            print("Autor não pode ser vazio. Tente novamente.")
            continue
        break

    while True:
        try:
            ano = int(input('Digite o ano do livro (ex: 2021): '))
            if ano < 0:  # Verifica se o ano é negativo
                print("O ano não pode ser negativo. Tente novamente.")
                continue
        except ValueError:
            print("Entrada inválida. Digite um ano válido.")
            continue
        break

    while True:
        try:
            preco = float(input('Digite o preço do livro: '))
            if preco < 0:  # Verifica se o preço é negativo
                print("O preço não pode ser negativo. Tente novamente.")
                continue
        except ValueError:
            print("Entrada inválida. Digite um preço válido.")
            continue
        break

    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano, preco)
        VALUES (?,?,?,?)
    
    ''',(titulo,autor,ano,preco))

    print('\n\nNovo livro adicionado com sucesso!\n')
    print(
        f'titulo: {titulo}  autor: {autor}   ano: {ano}   preco: {preco}'
    )
    connect.commit()
    connect.close()

def exibir_livros():
    livros = get_livros()

    if livros:
        print("\nLivros disponíveis:")
        for livro in livros:
            print(f'ID: {livro[0]}  Título: {livro[1]}  Autor: {livro[2]}  Ano: {livro[3]}  Preço: {livro[4]:.2f}')
    else:
        print("\nNenhum livro encontrado.")

    return livros

def att_preco_livro():
    exibir_livros()
    
    id = int(input('selecione o id do livro a ser atualizado: '))
    preco = float(input('digite o novo preço do livro: '))

    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        UPDATE livros SET preco = ? WHERE ID = ?
    
    ''',(preco,id))

    print('Preço atualizado com sucesso!')
    connect.commit()
    connect.close()

def remover_livro():
    exibir_livros()

    id = int(input('selecione o id do livro a ser deletado: '))

    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        DELETE FROM livros WHERE ID = ?
    
    ''',(id,))
    print('Livro deletado com sucesso! ')

    connect.commit()
    connect.close()

def buscar_livro_por_autor():
    autor = input('Digite o nome do autor que você deseja filtrar os livros: ')

    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        SELECT * FROM livros WHERE autor = ?
    ''',(autor,))
    livros = cursor.fetchall()

    if livros:
        print(f"\nLivros disponíveis do autor: {autor}")
        for livro in livros:
            print(f'ID: {livro[0]}  Título: {livro[1]}  Autor: {livro[2]}  Ano: {livro[3]}  Preço: {livro[4]:.2f}')
    else:
        print("\nNenhum livro encontrado.")
    
    connect.close()

def exportar_csv():
    livros = get_livros()

    os.makedirs("exports", exist_ok=True)

    with open('exports/livros.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        escritor_csv = csv.writer(csvfile)
        escritor_csv.writerow(['ID', 'Titulo', 'Autor', 'Ano', 'Preco'])
        
        for livro in livros:
            escritor_csv.writerow(livro)

def importar_csv():
    with open('exports/livros.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        leitor_csv = csv.reader(csvfile)
        header = next(leitor_csv)  # Lê o cabeçalho

        # Verifica se os cabeçalhos estão corretos
        if header != ['ID', 'Titulo', 'Autor', 'Ano', 'Preco']:
            print("Cabeçalhos do CSV não correspondem ao esperado.")
            return

        livros = []
        for linha in leitor_csv:
            livro = {
                'id': int(linha[0]),
                'titulo': linha[1],
                'autor': linha[2],
                'ano': int(linha[3]),
                'preco': float(linha[4])
            }
            livros.append(livro)

        connect = sqlite3.connect('livraria.db')
        cursor = connect.cursor()

        for livro in livros:
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano, preco)
                VALUES (?,?,?,?)
            
            ''',(livro["titulo"],livro["autor"],livro["ano"],livro["preco"]))
        connect.commit()
        connect.close()
        print(f"{len(livros)} livros foram adicionados ao banco de dados")

def get_livros():
    connect = sqlite3.connect('livraria.db')
    cursor = connect.cursor()
    cursor.execute('''
        SELECT * FROM livros
    ''')
    livros = cursor.fetchall()
    connect.close()
    return livros

def backup():
    os.makedirs("backup", exist_ok=True)

    nome = f'backup_{datetime.now().strftime("%Y%m%d")}.db'
    with open('livraria.db', 'rb') as arquivo_original:
        with open('backup/' + nome, 'wb') as arquivo_backup:
            arquivo_backup.write(arquivo_original.read())

def main():
    iniciar_banco()

    while True:
        print("""
        1. Adicionar novo livro
        2. Exibir todos os livros
        3. Atualizar preço de um livro
        4. Remover um livro
        5. Filtrar por autor
        6. Exportar para CSV
        7. Importar CSV
        8. Backup do banco
        9. Sair
        """)
        
        try:
            opcao = int(input('Selecione uma opção: '))
            match opcao:
                case 1:
                    novo_livro()
                case 2:
                    exibir_livros()
                case 3:
                    att_preco_livro()
                case 4:
                    remover_livro()
                case 5:
                    buscar_livro_por_autor()
                case 6:
                    exportar_csv()
                case 7:
                    importar_csv()
                case 8:
                    backup()
                case 9:
                    return
                case _:
                    print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

main()

