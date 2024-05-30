from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

janela = Tk()

# NAVE DE ESCOLTA (BATEDOR)
class Validadores:
    # VALIDANDO A ENTRADA DA ENTRY CODIGO.
    def validate_entrycod(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 10000

    # VALIDANDO A ENTRY TELEFONE.
    def validate_entry_telefone(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100000000000
    
    # VALIDANDO A ENTRY NOME.
    def validate_entry_nome(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 60:
                return True
            else:
                return False
    
    # VALIDANDO A ENTRY CIDADE.
    def validate_entry_cidade(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 30:
                return True
            else:
                return False
            
    def valida_entryidbook(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 10000
    
    # FUNÇÃO REFERENTE AO CAMPO ANO DE PUBLICAÇÃO
    def validate_entryanopubli(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 10000
    
    # FUNÇÃO REFERENTE AO CAMPO DE QUANTIDADE DE LIVROS.
    def validate_entryqtdlivro(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100
    
    # CRIANDO OS VALIDADORES REFERENTE AS ENTRYS QUE UTILIZAM TEXTO, TITULO DO LIVRO, NOME DO AUTOR.
    # FUNÇÃO REFERENTE AO CAMPO TITULO DO LIVRO.
    def validate_entry_titulolivro(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 65:
                return True
            else:
                return False
            
    # FUNÇÃO REFERENTE AO CAMPO DE QUANTIDADE DE LIVROS.
    def validate_entry_nameautor(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 35:
                return True
            else:
                return False
            
# NAVE DE RETAGUARDA. (OFICIAL RESERVA).
class Relatorios:
    def printCliente(self):
        webbrowser.open('Cliente.pdf')

    # GERA O RELATORIO DE APENAS UM USUARIO.    
    def gerarRelatCliente(self):
        self.c = canvas.Canvas('Cliente.pdf')

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(35, 700, 'Codigo: ')
        self.c.drawString(35, 675, 'Nome: ')
        self.c.drawString(35, 650, 'Telefone: ')
        self.c.drawString(35, 625, 'Cidade: ')
        
        self.c.setFont('Helvetica', 18)        
        self.c.drawString(109, 700, self.codigoRel)
        self.c.drawString(98, 675, self.nomeRel)
        self.c.drawString(118, 650, self.telefoneRel)
        self.c.drawString(107, 625, self.cidadeRel)

        #self.c.rect(20, 258, 550, 350, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

    # FUNÇÃO QUE ABRIRA O RELATORIO DO LIVRO.
    def printLivro(self):
        webbrowser.open('Livros.pdf')

    # GERA O RELATORIO DE UM LIVRO DA BIBLIOTECA.
    def gerarRelatLivro(self):
        self.c = canvas.Canvas('Livros.pdf')

        self.idlivroRel = self.idbook_entry.get()
        self.tituloRel = self.nomelivro_entry.get()
        self.autorlivroRel = self.autorlivro_entry.get()
        self.anopubliRel = self.anopubli_entry.get()
        self.qtdRel = self.qtdlivro_entry.get()

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(200, 790, 'Ficha do Livro')

        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(32, 700, 'Codigo: ')
        self.c.drawString(32, 675, 'Titulo do livro: ')
        self.c.drawString(32, 650, 'Autor: ')
        self.c.drawString(32, 625, 'Ano Publicação: ')
        self.c.drawString(32, 600, 'Qtd Disponivel: ')
        
        self.c.setFont('Times-Roman', 16)        
        self.c.drawString(104, 700, self.idlivroRel)
        self.c.drawString(163, 675, self.tituloRel)
        self.c.drawString(95, 650, self.autorlivroRel)
        self.c.drawString(177, 625, self.anopubliRel)
        self.c.drawString(169, 600, self.qtdRel)

        #self.c.rect(20, 258, 550, 350, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printLivro()

    # FUNÇÃO QUE ABRIRA O INVENTARIO GERAL DA BIBLIOTECA.
    def printInventario(self):
        webbrowser.open('Inventario da Biblioteca.pdf')
    
    # CONFIGURAÇÃO SQLITE PARA GERAR O RELATORIO GERAL.
    def callSQL(self):
        self.conn = sqlite3.connect('Dados Gerais Biblioteca.bd')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT id, titulo, autor, ano_publi, quantidade FROM livros")
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    # GERANDO O RELATORIO GERAL DOS LIVROS.
    def geraRelatINVENTARIO_LIVROS(self):
        data = self.callSQL()
        self.c = canvas.Canvas("Inventario da Biblioteca.pdf")
        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(160,790,'Inventário da Biblioteca')

        self.c.setFont('Helvetica-Bold', 12)
        self.c.drawString(30, 760, 'ID')
        self.c.drawString(150, 760, 'Título')
        self.c.drawString(350, 760, 'Autor')
        self.c.drawString(465, 760, 'Ano Pub')
        self.c.drawString(526, 760, 'Quant.')

        y=745
        self.c.setFont('Helvetica', 12)
        for id, titulo, autor, ano_publi, quantidade in data:
            self.c.drawString(30, y, str(id))
            self.c.drawString(80, y, str(titulo)[:35])
            self.c.drawString(330, y, str(autor))
            self.c.drawString(475, y, str(ano_publi))
            self.c.drawString(545, y, str(quantidade))
            y -= 20

            if y < 50: # CASO PRECISE DE UMA NOVA PAGINA
                self.c.setFont('Helvetica-Bold', 10)
                self.c.drawString(30, 800, 'ID')
                self.c.drawString(150, 800, 'Título')
                self.c.drawString(200, 800, 'Autor')
                self.c.drawString(220, 800, 'Ano Pub.')
                self.c.drawString(400, 800, 'Quant.')
                y = 780  # RESETA A POSIÇÃO Y A CADA PAGINA NOVA.
            
        self.c.showPage()
        self.c.save()
        self.printInventario()

    # FUNÇÃO QUE ABRIRA O INVENTARIO DOS CLIENTES.
    def printInvent_CLIENTES(self):
        webbrowser.open('Relatorio Geral dos Clientes.pdf')
    
    # CONFIGURAÇÃO DO SQLITE PARA CONEXÃO COM A TABELA CLIENTES.
    def call_to_SQL(self):
        self.conn = sqlite3.connect('Dados Gerais Biblioteca.bd')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM clientes")
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    # GERANDO O RELATORIO GERAL DOS CLIENTES.
    def geraRelatINVENTARIO_CLIENTES(self):
        data = self.call_to_SQL()
        self.c = canvas.Canvas("Relatorio Geral dos Clientes.pdf")
        self.c.setFont('Helvetica-Bold', 24)

        self.c.drawString(160, 790, 'Inventário de Clientes')
        self.c.setFont('Helvetica-Bold', 12)
        self.c.drawString(30, 760, 'ID')
        self.c.drawString(60, 760, 'Nome Cliente')
        self.c.drawString(350, 760, 'Telefone')
        self.c.drawString(475, 760, 'Cidade')

        y=745
        self.c.setFont('Helvetica', 12)
        for cod, nome_cliente, telefone, cidade in data:
            self.c.drawString(30, y, str(cod))
            self.c.drawString(60, y, str(nome_cliente))
            self.c.drawString(330, y, str(telefone))
            self.c.drawString(475, y,str(cidade))
            y -= 20

            if y < 50: # CASO PRECISE DE UMA NOVA PAGINA.
                self.c.setFont('Helvetica-Bold', 16)
                self.c.drawString(30, 800, 'ID')
                self.c.drawString(150, 800, 'Nome Cliente')
                self.c.drawString(200, 800, 'Telefone')
                self.c.drawString(260, 800, 'Cidade')
                y = 780 # RESETA A POSIÇÃO Y A CADA PAGINA NOVA.

        self.c.showPage()
        self.c.save()
        self.printInvent_CLIENTES()

# NAVE DE ESCOLTA (SEGUNDO COMANDANTE)
class Funcs_Empres_Devol:  
    # FUNÇÃO QUE IRA LIMPAR TODOS OS CAMPOS TANTO DE EMPRESTIMOS QUANTO DE DEVOLUÇÃO.
    def limpar_todos_campos(self):
        self.idtransacao_entry.delete(0, END)
        self.nomedocliente_entry.delete(0, END)
        self.contatocliente_entry.delete(0, END)
        self.titulodolivro_entry.delete(0, END)
        self.qtdretirada_entry.delete(0, END)
        self.dataretirada_entry.delete(0, END)
        self.idtransacaof2_entry.delete(0, END)
        self.clientnamef2_entry.delete(0, END)
        self.titulivrof2_entry.delete(0, END)
        self.qtdDEVOLf2_entry.delete(0, END)
        self.dataDEVOLf2_entry.delete(0, END)

    # FUNÇÃO QUE CONECTA O BANCO DE DADOS E CRIA O BANCO DE DADOS (CASO NÃO EXISTA).
    def conecta_bd(self):
        self.conn = sqlite3.connect('Dados Gerais Biblioteca.bd')
        self.cursor = self.conn.cursor()

    # FUNÇÃO QUE DESCONECTA O BANDO DE DADOS.
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando do Banco de Dados Gerais da Biblioteca.')

    # FUNÇÃO QUE IRA CONCENTRAR TODAS AS VARIAVEIS GET TANTO DE EMPRESTIMOS QUANTO DE DEVOLUÇÃO.
    def variaveis_Empres_Devol(self):
        self.idtransacao = self.idtransacao_entry.get()
        self.nomedocliente = self.nomedocliente_entry.get()
        self.contatocliente = self.contatocliente_entry.get()
        self.titulodolivro = self.titulodolivro_entry.get()
        self.qtdretirada = self.qtdretirada_entry.get()
        self.dataretirada = self.dataretirada_entry.get()
        self.idtransacaof2 = self.idtransacaof2_entry.get()
        self.clientnamef2 = self.clientnamef2_entry.get()
        self.titulolivrof2 = self.titulivrof2_entry.get()
        self.qtdDEVOLf2 = self.qtdDEVOLf2_entry.get()
        self.dataDEVOLf2 = self.dataDEVOLf2_entry.get()

    # FUNÇÃO PARA ADICIONAR LIVROS NA TREEVIEW EMPRESTIMOS.
    def add_Livros_Empres(self):
        self.variaveis_Empres_Devol()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO emprestimos (quantidade_retirada, nome_cliente, titulo_livro, telefone, data_retirada)
            VALUES (?, ?, ?, ?, ?)""",(self.qtdretirada, self.nomedocliente, self.titulodolivro, self.contatocliente, self.dataretirada))
        self.conn.commit()
        self.desconecta_bd()
        self.select_Livros_Empres()
        self.limpar_todos_campos()

    # SELECIONANDO A LISTA DA TREEVIEW DE LIVROS EMPRESTADOS.
    def select_Livros_Empres(self):
        self.listaEmprestimo.delete(*self.listaEmprestimo.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT id_transacao, quantidade_retirada, nome_cliente, titulo_livro, telefone, data_retirada FROM emprestimos
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaEmprestimo.insert('', END, values=i)
        self.desconecta_bd()

    # ADICIONAR LIVROS NA TREEVIEW DE DEVOLUÇÃO.
    def add_Livros_Devol(self):
        self.variaveis_Empres_Devol()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO devolucao (quantidade_devolvida, nome_cliente, titulo_livro, data_devolucao)
            VALUES (?, ?, ?, ?)""",(self.clientnamef2, self.titulolivrof2, self.qtdDEVOLf2, self.dataDEVOLf2))
        self.conn.commit()
        self.desconecta_bd()
        self.select_Livros_Devol()
        self.limpar_todos_campos()

    # SELECIONANDO A LISTA DA TREEVIEW DE LIVROS DEVOLVIDOS.
    def select_Livros_Devol(self):
        self.listaDevolucao.delete(*self.listaDevolucao.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT id_transacao, quantidade_devolvida, nome_cliente, titulo_livro, data_devolucao FROM devolucao
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaDevolucao.insert('', END, values=i)
        self.desconecta_bd()

    # FUNÇÃO PARA CONFIRMAR EMPRESTIMO E ATUALIZAR A COLUNA DE QUANTIDADE DISPONIVEL SUBTRAINDO PELA QUANTIDADE RETIRADA.
    def confirmar_emprestimo(self):
        try:
            self.conecta_bd()
            self.variaveis_Empres_Devol()
            self.cursor.execute("BEGIN TRANSACTION;")
            self.cursor.execute("SELECT quantidade FROM livros WHERE titulo = ?", (self.titulodolivro,))
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] >= int(self.qtdretirada):
                nova_quantidade_disponivel = resultado[0] - int(self.qtdretirada)
                self.cursor.execute("UPDATE livros SET quantidade = ? WHERE titulo = ?", (nova_quantidade_disponivel, self.titulodolivro))
                self.cursor.execute("INSERT INTO emprestimos (quantidade_retirada, nome_cliente, titulo_livro, telefone, data_retirada) VALUES (?, ?, ?, ?, ?)",
                                    (self.qtdretirada, self.nomedocliente, self.titulodolivro, self.contatocliente, self.dataretirada))
                self.conn.commit()
                print('emprestimo confirmado.')
            else:
                print('Quantidade de livros insuficiente, emprestimo negado.')
                self.conn.rollback()

            self.add_Livros_Empres()
        except Exception as e:
            print(f'Ocorreu um erro {e}')
            self.conn.rollback()
        finally:
            self.desconecta_bd()
            self.limpar_todos_campos()

    # CONFIRMANDO A DEVOLUÇÃO E ATUALIZANDO A QUANTIDADE DISPONIVEL.
    def confirmar_devolucao(self):
        try:
            self.conecta_bd()
            self.variaveis_Empres_Devol()
            self.cursor.execute("BEGIN TRANSACTION;")
            self.cursor.execute("SELECT quantidade FROM livros WHERE titulo = ?", (self.titulolivrof2,))
            result = self.cursor.fetchone()
            if result[0] >= int(self.qtdDEVOLf2):
                # ATUALIZA A QUANTIDADe DE LIVROS.
                new_qtd_dispo = result[0] + int(self.qtdDEVOLf2)
                self.cursor.execute("UPDATE livros SET quantidade = ? WHERE titulo = ?", (new_qtd_dispo, self.titulolivrof2))
                # REGISTRA A DEVOLUÇÃO.
                self.cursor.execute("INSERT INTO devolucao (quantidade_devolvida, nome_cliente, titulo_livro, data_devolucao) VALUES (?, ?, ?, ?)",
                                    (self.qtdDEVOLf2, self.clientnamef2, self.titulolivrof2, self.dataDEVOLf2))
                # DELETA O REGISTRO DE EMPRESTIMO.
                self.cursor.execute("DELETE FROM emprestimos WHERE nome_cliente = ? AND titulo_livro = ? AND quantidade_retirada = ?",
                                    (self.nomedocliente, self.titulodolivro, self.qtdretirada))
                self.conn.commit()
                print('Devolução Feita com Sucesso.')
            else:
                print('Aparentemente tivemos um erro.')
                self.conn.rollback()

            self.add_Livros_Devol()
        except Exception as e:
            print(f'Ocorreu um erro {e}')
            self.conn.rollback()
        finally:
            self.desconecta_bd()
            self.limpar_todos_campos()
           
# NAVE DE ESCOLTA (BATEDOR CHEFE)
class Funcs_Gerais:
    # ADICIONANDO A FUNÇÃO DE LIMPAR TODOS OS CAMPOS DA BIBLIOTECA.
    def limpar_campos(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.idbook_entry.delete(0, END)
        self.nomelivro_entry.delete(0, END)
        self.autorlivro_entry.delete(0, END)
        self.anopubli_entry.delete(0, END)
        self.qtdlivro_entry.delete(0, END)

    # FUNÇÃO QUE CONECTA O BANCO DE DADOS.
    def conecta_bd(self):
        self.conn = sqlite3.connect('Dados Gerais Biblioteca.bd')
        self.cursor = self.conn.cursor()

    # FUNÇÃO QUE DESCONECTA O BANDO DE DADOS.
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando do Banco de Dados Gerais da Biblioteca.')

    # FUNÇÃO QUE IRA CRIAR AS TABELAS DE CLIENTES E LIVROS DA BIBLIOTECA.
    def montarTabela(self):
        self.conecta_bd()
        # CRIAR AS TABELAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_usuario CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT,
            ano_publi INTEGER,
            quantidade INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade_retirada INTEGER (5),
                nome_cliente CHAR (60) NOT NULL,
                titulo_livro CHAR (60),
                telefone INTEGER (12),
                data_retirada DATE      
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS devolucao (
                id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade_devolvida INTEGER (5),
                nome_cliente CHAR (60) NOT NULL,
                titulo_livro CHAR(60),
                data_devolucao DATE                
            );
        """)
        
        self.conn.commit(); print('As tabelas foram criadas com sucesso.')
        self.desconecta_bd()

    # CRIANDO UMA FUNÇÃO PARA ABRIGAR VARIAVEIS FACILITANDO PARA QUANDO FOR UTILIZAR POSTERIORMENTE.
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.idbook = self.idbook_entry.get()
        self.titulo = self.nomelivro_entry.get()
        self.autor = self.autorlivro_entry.get()
        self.anopubli = self.anopubli_entry.get()
        self.qtd = self.qtdlivro_entry.get()

    # FUNÇÃO QUE IRA ADICIONAR CLIENTES E SOMENTE CLIENTES.
    def add_usuarios(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_usuario, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.seleciona_lista()
        self.limpar_campos()

    # SELECIONANDO A LISTA PARA ADICIONAR AS INFORMAÇÕES SOBRE OS CLIENTES.    
    def seleciona_lista(self):
        self.listaCliente.delete(*self.listaCliente.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_usuario, telefone, cidade FROM clientes
            ORDER BY nome_usuario ASC; """)
        for i in lista:
            self.listaCliente.insert('', END, values=i)
        self.desconecta_bd()

    # CRIANDO A FUNÇÃO PARA ADICIONAR LIVROS
    def insert_book(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("INSERT INTO livros (titulo, autor, ano_publi, quantidade) VALUES (?, ?, ?, ?)", (self.titulo, self.autor, self.anopubli, self.qtd))

        self.conn.commit()
        self.desconecta_bd()
        self.select_Lista_Livros()
        self.limpar_campos()

    # CRIANDO A SELEÇÃO DA LISTA DE LIVROS.
    def select_Lista_Livros(self):
        self.listaLivros.delete(*self.listaLivros.get_children())
        self.conecta_bd()
        listaJ2 = self.cursor.execute("""SELECT id, titulo, autor, ano_publi, quantidade FROM livros
            ORDER BY titulo ASC; """)
        for i in listaJ2:
            self.listaLivros.insert('', END, values=i)
        self.desconecta_bd()

    # ADICIONANDO A FUNÇÃO DE CLIQUE DUPLO PARA SELECIONAR UM LIVRO NA TREEVIEW FRAME 4.
    def Clique_Duplo(self, event):
        self.listaLivros.selection()

        for n in self.listaLivros.selection():
            values = self.listaLivros.item(n, 'values')
            if len(values) == 5:
                col1, col2, col3, col4, col5 = values
                self.idbook_entry.insert(END, col1)
                self.nomelivro_entry.insert(END, col2)
                self.autorlivro_entry.insert(END, col3)
                self.anopubli_entry.insert(END, col4)
                self.qtdlivro_entry.insert(END, col5)

    # ADICIONANDO A FUNÇÃO DE CLIQUE DUPLO PARA SELECIONAR CLIENTES NA TREEVIEW DO FRAME 2.
    def Clique_Duplo_Cli(self, event):
        self.listaCliente.selection()

        for n in self.listaCliente.selection():
            col1, col2, col3, col4 = self.listaCliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
        
    # CRIANDO A FUNÇÃO DO BOTÃO ALTERAR CADASTRO DO CLIENTE.
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_usuario = ?, telefone = ?, cidade = ?
            WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.seleciona_lista()
        self.limpar_campos()

    # CRIANDO A FUNÇÃO DO BOTÃO ALTERAR CADASTRO DE LIVROS.
    def altera_livros(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE livros SET titulo = ?, autor = ?, ano_publi = ?, quantidade = ?
            WHERE id = ?""", (self.titulo, self.autor, self.anopubli, self.qtd, self.idbook))
        self.conn.commit()
        self.select_Lista_Livros()
        self.limpar_campos()

    # CRIANDO A FUNÇÀO DO BOTÀO BUSCAR.
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCliente.delete(*self.listaCliente.get_children())

        self.nome_entry.insert(END, '%')   
        nome = self.nome_entry.get() + '%'
        self.cursor.execute(
            """ SELECT cod, nome_usuario, telefone, cidade FROM clientes
            WHERE nome_usuario LIKE ? ORDER BY nome_usuario ASC""", (nome,))
        buscanomeCliente = self.cursor.fetchall()
        for i in buscanomeCliente:
            self.listaCliente.insert("", END, values=i)          
        self.limpar_campos()
        self.desconecta_bd()    
        print(buscanomeCliente)

    # CRIANDO A FUNÇÃO DE BUSCAR LIVRO.
    def busca_livro(self):
        self.conecta_bd()
        self.listaLivros.delete(*self.listaLivros.get_children())

        titulo = self.nomelivro_entry.get()
        autor = self.autorlivro_entry.get()
        anopubli = self.anopubli_entry.get()

        titulo = titulo + '%' if titulo else ''
        autor = autor + '%' if autor else ''
        anopubli = anopubli + '%' if anopubli else ''

        self.cursor.execute(
            """SELECT id, titulo, autor, ano_publi, quantidade  FROM livros
            WHERE titulo LIKE ? OR autor LIKE ? OR ano_publi LIKE ? ORDER BY titulo""", (titulo, autor, anopubli))
        buscamultiLivro = self.cursor.fetchall()
        for n in buscamultiLivro:
            self.listaLivros.insert("", END, values=n)
        self.limpar_campos()
        self.desconecta_bd()
        print(f"O {titulo}, O {autor}, O {anopubli}, E O PRINCIPAL {buscamultiLivro}")

    # CRIANDO UMA FUNÇÃO QUE IRA ATUALIZAR O CAMPO CODIGO. EX: USUARIO 2 É EXCLUIDO O USUARIO 3 OS QUE OS SUCEDEREM DEVEM 'SUBIR' NA LISTA
    def atualizar_codigos_clientes(self):
        self.variaveis()
        self.conecta_bd()
        clientes = self.cursor.execute("SELECT cod FROM clientes ORDER BY cod").fetchall()
        for i, clientes in enumerate(clientes, start=1):
            self.cursor.execute('UPDATE clientes SET cod = ? WHERE cod = ?',(i, clientes[0]))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_campos()
        self.seleciona_lista()

    # CRIANDO A FUNÇÃO DO BOTÃO DELETAR CLIENTES.
    def deleta_usuario(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.atualizar_codigos_clientes()
        self.limpar_campos()
        self.seleciona_lista()

    # ADICIONANDO A FUNÇÃO DE DELETAR LIVRO(ESTA FUNÇÃO ESTARA DISPONIVEL NO MENUBAR CLICANDO EM OPÇÕES).
    def deleta_livro(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM livros WHERE id = ? """, (self.idbook,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_campos()
        self.select_Lista_Livros()
    
# NAVE DE ARTILHARIA (APOIO BELICO NAVE MÃE)
class Janela2(Funcs_Empres_Devol):
    def invocar_Janela2(self):
        self.criacaoJanela2()
        self.frames_Janela2()
        self.widgets_frame1_Janela2()
        self.lista_frameTres_Janela2()
        self.widgets_frame2_Janela2()
        self.lista_frameQuatro_Janela2()
        self.select_Livros_Empres()
        self.select_Livros_Devol()

    # CONFIGURAÇÕES DA JANELA PARA EMPRESTIMO E DEVOLUÇÃO.
    def criacaoJanela2(self):
        self.Janela2 = Toplevel()
        self.Janela2.title = ("Sistema Para Emprestimo e Devolução de Livros")
        self.Janela2.configure(background= 'lightblue')
        self.Janela2.geometry('1500x800')
        self.Janela2.resizable(False, False)
        self.Janela2.transient(self.janela)
        self.Janela2.focus_force()
        self.Janela2.grab_set()

    # CRIANDO 2 FRAMES PARA ABRIGAR AS ENTRYS E LABELS PARA EMPRESTIMO E DEVOLUÇÃO.
    def frames_Janela2(self):
        self.frameUM = Frame(self.Janela2, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frameUM.place(relx=0.01, rely=0.02, relwidth=0.49, relheight=0.46)

        self.frameDois = Frame(self.Janela2, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frameDois.place(relx=0.01, rely=0.5, relwidth=0.49, relheight=0.46)

        self.frameTres = Frame(self.Janela2, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frameTres.place(relx=0.51, rely=0.02, relwidth=0.47, relheight=0.46)

        self.frameQuatro = Frame(self.Janela2, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frameQuatro.place(relx=0.51, rely=0.5, relwidth=0.47, relheight=0.46)

    # CRIANDO DEF ONDE IRA ABRIGAR AS LABELS E BOTÕES PARA EMPRESTIMO.
    def widgets_frame1_Janela2(self):
        # CRIANDO O BOTÃO DE EMPRESTIMO DO LIVRO.
        self.bt_emprestimo = Button(self.frameUM, text= 'Confirmar Emprestimo do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'),command=self.confirmar_emprestimo)
        self.bt_emprestimo.place(relx=0.3, rely=0.85, relwidth=0.3, relheight=0.11)

        # INSERINDO UM BOTÃO PARA LIMPAR TODOS OS CAMPOS.
        self.btdeleteall = Button(self.frameUM, text= 'Limpar todos os campos', bd=2, bg='#107db2',fg='white', font=('verdana', 8, 'bold'), command=self.limpar_todos_campos)
        self.btdeleteall.place(relx=0.65, rely=0.85, relwidth=0.3, relheight=0.11)

        # LABEL E ENTRADA DO CAMPO ID TRANSAÇÃO.
        self.lb_idtransacao = Label(self.frameUM, text='ID Transação: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_idtransacao.place(relx=0.02, rely=0.04)

        self.idtransacao_entry = Entry(self.frameUM)
        self.idtransacao_entry.place(relx=0.15, rely=0.04, relwidth=0.08, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO NOME CLIENTE.
        self.lb_nomedocliente = Label(self.frameUM, text='Nome Cliente: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_nomedocliente.place(relx=0.02, rely=0.16)

        self.nomedocliente_entry = Entry(self.frameUM)
        self.nomedocliente_entry.place(relx=0.15, rely=0.16, relwidth=0.5, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO TELEFONE.
        self.lb_contatocliente = Label(self.frameUM, text='Telefone: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_contatocliente.place(relx=0.02, rely=0.28)

        self.contatocliente_entry = Entry(self.frameUM)
        self.contatocliente_entry.place(relx=0.15, rely=0.28, relwidth=0.11, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO TITULO DO LIVRO.
        self.lb_titulodolivro = Label(self.frameUM, text='Titulo do Livro: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_titulodolivro.place(relx=0.02, rely=0.40)

        self.titulodolivro_entry = Entry(self.frameUM, bg= '#dfe3ee', fg= '#107db2')
        self.titulodolivro_entry.place(relx=0.15, rely=0.40, relwidth=0.5, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO QUANTIDADE RETIRADA.
        self.lb_qtdretirada = Label(self.frameUM, text='Qtd Retirada', bg= '#dfe3ee', fg= '#107db2')
        self.lb_qtdretirada.place(relx=0.02, rely=0.52)

        self.qtdretirada_entry = Entry(self.frameUM)
        self.qtdretirada_entry.place(relx=0.15, rely=0.52, relwidth=0.12, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO DATA RETIRADA.
        self.lb_dataretirada = Label(self.frameUM, text='Data Retirada: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_dataretirada.place(relx=0.02, rely=0.64)

        self.dataretirada_entry = Entry(self.frameUM)
        self.dataretirada_entry.place(relx=0.15, rely=0.64, relwidth=0.12, relheight=0.06)

    # CRIANDO TREEVIEW RELACIONADA A EMPRESTIMO.
    def lista_frameTres_Janela2(self):
        self.listaEmprestimo = ttk.Treeview(self.frameTres, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.listaEmprestimo.heading('#0', text='')
        self.listaEmprestimo.heading('#1', text='ID Transação')
        self.listaEmprestimo.heading('#2', text='Qtd Retirada')
        self.listaEmprestimo.heading('#3', text='Nome Cliente')
        self.listaEmprestimo.heading('#4', text='Titulo do Livro')
        self.listaEmprestimo.heading('#5', text='Telefone')
        self.listaEmprestimo.heading('#6', text='Data Retirada')

        self.listaEmprestimo.column('#0', width=1)        
        self.listaEmprestimo.column('#1', width=1)
        self.listaEmprestimo.column('#2', width=51)
        self.listaEmprestimo.column('#3', width=150)
        self.listaEmprestimo.column('#4', width=150)
        self.listaEmprestimo.column('#5', width=50)
        self.listaEmprestimo.column('#6', width=48)

        self.listaEmprestimo.place(relx= 0.01, rely= 0.01, relwidth= 0.955, relheight= 0.98)

        self.scroolLista = Scrollbar(self.frameTres, orient= 'vertical')
        self.listaEmprestimo.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.965, rely= 0.01, relwidth= 0.031, relheight=0.98)

    # CRIANDO DEF ONDE IRA ABRIGAR AS LABELS E BOTÕES PRA DEVOLUÇÃO.
    def widgets_frame2_Janela2(self):
        # CRIANDO O BOTÃO DE DEVOLUÇÃO DO LIVRO.
        self.bt_devolucao = Button(self.frameDois, text= 'Confirmar Devolução do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.confirmar_devolucao)
        self.bt_devolucao.place(relx=0.3, rely=0.85, relwidth=0.38, relheight=0.11)

        # LABEL E ENTRADA DO CAMPO ID TRANSAÇÃO.
        self.lb_idtransacaof2 = Label(self.frameDois, text='ID Transação: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_idtransacaof2.place(relx=0.02, rely=0.04)

        self.idtransacaof2_entry = Entry(self.frameDois)
        self.idtransacaof2_entry.place(relx=0.16, rely=0.04, relwidth=0.12, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO NOME CLIENTE.
        self.lb_clientnamef2 = Label(self.frameDois, text='Nome Cliente: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_clientnamef2.place(relx=0.02, rely=0.18)

        self.clientnamef2_entry = Entry(self.frameDois)
        self.clientnamef2_entry.place(relx=0.16, rely=0.18, relwidth=0.5, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO TITULO DO LIVRO.
        self.lb_titulivrof2 = Label(self.frameDois, text='Titulo do Livro: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_titulivrof2.place(relx=0.02, rely=0.32)

        self.titulivrof2_entry = Entry(self.frameDois)
        self.titulivrof2_entry.place(relx=0.16, rely=0.32, relwidth=0.5, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO QUANTIDADE DEVOLVIDA.
        self.lb_qtdDEVOLf2 = Label(self.frameDois, text='Qtd Devolvida: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_qtdDEVOLf2.place(relx=0.02, rely=0.46)

        self.qtdDEVOLf2_entry = Entry(self.frameDois)
        self.qtdDEVOLf2_entry.place(relx=0.16, rely=0.46, relwidth=0.12, relheight=0.06)

        # LABEL E ENTRADA DO CAMPO DATA DEVOLUÇÃO.
        self.lb_dataDEVOLf2 = Label(self.frameDois, text='Data Devolução: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_dataDEVOLf2.place(relx=0.02, rely=0.60)

        self.dataDEVOLf2_entry = Entry(self.frameDois)
        self.dataDEVOLf2_entry.place(relx=0.16, rely=0.60, relwidth=0.12, relheight=0.06)
    
    # CRIANDO TREEVIEW RELACIONADA A DEVOLUÇÃO.
    def lista_frameQuatro_Janela2(self):
        self.listaDevolucao = ttk.Treeview(self.frameQuatro, height= 3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaDevolucao.heading('#0', text='')
        self.listaDevolucao.heading('#1', text='ID Transação')

        self.listaDevolucao.heading('#2', text='Qtd Devolvida')
        self.listaDevolucao.heading('#3', text='Nome Cliente')
        self.listaDevolucao.heading('#4', text='Titulo do Livro')
        self.listaDevolucao.heading('#5', text='Data Devolução')
        

        self.listaDevolucao.column('#0', width=1)        
        self.listaDevolucao.column('#1', width=5)
        self.listaDevolucao.column('#2', width=50)
        self.listaDevolucao.column('#3', width=198)
        self.listaDevolucao.column('#4', width=197)
        self.listaDevolucao.column('#5', width=50)

        self.listaDevolucao.place(relx= 0.01, rely= 0.01, relwidth= 0.955, relheight= 0.98)

        self.scroolLista = Scrollbar(self.frameQuatro, orient= 'vertical')
        self.listaEmprestimo.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.965, rely= 0.01, relwidth= 0.031, relheight=0.98)

#  NAVE MÃE (INTER-ESTRELAR)
class App_Biblioteca(Janela2, Funcs_Gerais, Funcs_Empres_Devol, Relatorios, Validadores):
    def __init__(self):
        self.janela = janela
        self.botao_confirmar_emprestimo = Button(self.janela, text="Confirmar Empréstimo", command=self.confirmar_emprestimo_gui)
        self.checkEntrys()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.lista_frame2()
        self.widgets_frame_3()
        self.lista_livros_frame_4()
        self.select_Lista_Livros()
        self.montarTabela()
        self.seleciona_lista()
        self.Menu()
        janela.mainloop()

    # FUNÇÃO RESPONSAVEL PELAS CONFIGURAÇÕES DA TELA
    def tela(self):
        self.janela.title('Sistema Integrado da Biblioteca')
        self.janela.configure(background= '#1e3743')
        self.janela.geometry('1500x900')
        self.janela.resizable(False, False)

    # CRIANDO OS CAMPOS    
    def frames(self):
        self.frame_1 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.01, rely=0.02, relwidth=0.49, relheight=0.46)
        
        self.frame_2 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.01, rely=0.5, relwidth=0.49, relheight=0.49)

        self.frame_3 = Frame(self.janela, background= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_3.place(relx=0.51, rely=0.02, relwidth=0.481, relheight=0.46)

        self.frame_4 = Frame(self.janela, background= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_4.place(relx=0.51, rely=0.5, relwidth=0.481, relheight=0.49)

    # CRIANDO BOTÕES
    def widgets_frame1(self):
        # CRIANDO O BOTÃO LIMPAR
        self.bt_limpar = Button(self.frame_1, text='Limpar todos os campos', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'),command=self.limpar_campos)
        self.bt_limpar.place(relx=0.03, rely=0.1, relwidth=0.23, relheight=0.15)
        # CRIANDO O BOTÃO BUSCAR
        self.bt_buscar = Button(self.frame_1, text='Buscar Cliente', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.33,rely=0.1,relwidth=0.14,relheight=0.15)
        # CRIANDO O BOTÃO NOVO
        self.bt_novo = Button(self.frame_1, text='Confirmar Novo Cadastro de Cliente', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.add_usuarios)
        self.bt_novo.place(relx=0.61,rely=0.1,relwidth=0.38,relheight=0.15)
        # CRIANDO O BOTÃO ALTERAR
        self.bt_alterar = Button(self.frame_1, text='Alterar Cadastro do Cliente', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'),command=self.altera_cliente)
        self.bt_alterar.place(relx=0.69, rely=0.58, relwidth=0.3, relheight=0.15)
        # CRIANDO O BOTÃO APAGAR
        self.bt_apagar = Button(self.frame_1, text='Excluir Cliente', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.deleta_usuario)
        self.bt_apagar.place(relx=0.80, rely=0.83, relwidth=0.19, relheight=0.13)

        # CRIANDO As LABELS E ENTRADA(entry) ou input no python DO CODIGO
        # LABEL E ENTRADA DO CAMPO CODIGO.
        self.lb_codigo = Label(self.frame_1, text='Código: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_codigo.place(relx=0.03, rely=0.33)

        self.codigo_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd1)
        self.codigo_entry.place(relx=0.12, rely=0.33, relwidth=0.08)

        # LABEL E ENTRADA DO CAMPO NOME.
        self.lb_nome = Label(self.frame_1, text='Nome: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_nome.place(relx=0.03, rely=0.46)

        self.nome_entry = Entry(self.frame_1, validate= 'key', validatecommand= self.vcmd3)
        self.nome_entry.place(relx=0.12, rely=0.46, relwidth=0.55)

        # LABEL E ENTRADA DO CAMPO TELEFONE.
        self.lb_telefone = Label(self.frame_1, text='Telefone com DDD: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_telefone.place(relx=0.03, rely=0.6)

        self.telefone_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd2)
        self.telefone_entry.place(relx=0.2, rely=0.6, relwidth=0.22)

        # LABEL E ENTRADA DO CAMPO CIDADE.
        self.lb_cidade = Label(self.frame_1, text='Cidade: ', bg= '#dfe3ee', fg= '#107db2')
        self.lb_cidade.place(relx=0.03, rely=0.73)

        self.cidade_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd4)
        self.cidade_entry.place(relx=0.17, rely=0.73, relwidth=0.25)

    # CRIANDO UMA TABELA PARA O FRAME 2.
    def lista_frame2(self):
        self.listaCliente = ttk.Treeview(self.frame_2, height= 3, column=('col1', 'col2', 'col3', 'col4'))
        self.listaCliente.heading('#0', text='')
        self.listaCliente.heading('#1', text='Código')
        self.listaCliente.heading('#2', text='Nome')
        self.listaCliente.heading('#3', text='Telefone')
        self.listaCliente.heading('#4', text='Cidade')

        self.listaCliente.column('#0', width=1)        
        self.listaCliente.column('#1', width=50)
        self.listaCliente.column('#2', width=200)
        self.listaCliente.column('#3', width=125)
        self.listaCliente.column('#4', width=125)

        self.listaCliente.place(relx= 0.01, rely= 0.05, relwidth= 0.95, relheight= 0.89)

        self.scroolLista = Scrollbar(self.frame_2, orient= 'vertical')
        self.listaCliente.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.05, relwidth= 0.031, relheight=0.89)
        self.listaCliente.bind('<Double-1>', self.Clique_Duplo_Cli)

    # CRIANDO WIDGETS PARA O FRAME 3.
    def widgets_frame_3(self):
        # CRIANDO BOTÃO DE CONFIRMAR CADASTRO DO LIVRO.
        self.bt_newbook = Button(self.frame_3, text= 'Confirmar Cadastro do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'),command=self.insert_book)
        self.bt_newbook.place(relx=0.7, rely=0.18, relwidth=0.29, relheight=0.11)

        # CRIANDO O BOTÃO DE BUSCAR LIVRO.
        self.bt_buscalivro = Button(self.frame_3, text= 'Buscar Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.busca_livro)
        self.bt_buscalivro.place(relx=0.85, rely=0.48, relwidth=0.14, relheight=0.11)

        # CRIANDO O BOTÃO DE ALTERAR CADASTRO DO LIVRO.
        self.bt_alterarlivro = Button(self.frame_3,text= 'Alterar Cadastro do livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.altera_livros)
        self.bt_alterarlivro.place(relx=0.75, rely=0.34, relwidth=0.24, relheight=0.11)

        # CRIANDO O BOTÃO DE EXCLUIR LIVRO.
        self.bt_deletbook = Button(self.frame_3, text= 'Excluir Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.deleta_livro)
        self.bt_deletbook.place(relx=0.849, rely=0.63, relwidth=0.14, relheight=0.11)

        # CRIANDO O BOTÃO DE EMPRESTIMO DO LIVRO.
        self.bt_emprestimo = Button(self.frame_3, text= 'Sistema Para Emprestimo e Devolução', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.invocar_Janela2)
        self.bt_emprestimo.place(relx=0.3, rely=0.85, relwidth=0.361, relheight=0.11)

        # CRIANDO AS LABELS E AS ENTRYS DO FRAME 3.
        self.lb_idbook = Label(self.frame_3, text= 'ID do Livro', bg= '#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_idbook.place(relx=0.02, rely=0.05, relwidth=0.16, relheight=0.07)

        self.idbook_entry = Entry(self.frame_3, validate='key', validatecommand= self.vecc)
        self.idbook_entry.place(relx=0.19, rely=0.05, relwidth=0.07)

        # CRIANDO LABEL E ENTRY DO CADASTRO DO LIVRO
        self.lb_newbook = Label(self.frame_3, text= 'Informaçòes do Livro', bg='#dfe3ee', fg='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_newbook.place(relx=0.39, rely=0.21, relwidth=0.22)

        self.lb_nomelivro = Label(self. frame_3, text='Título do Livro', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_nomelivro.place(relx=0.02, rely=0.32, relwidth=0.16, relheight=0.07)

        self.nomelivro_entry = Entry(self.frame_3, validate= 'key', validatecommand=self.vect)
        self.nomelivro_entry.place(relx=0.18, rely=0.32, relwidth=0.47, relheight=0.07)

        # CRIANDO A LABEL E A ENTRY DO NOME DO AUTOR.
        self.lb_autorlivro = Label(self.frame_3, text= 'Autor do Livro', bg='#dfe3ee', fg='#107db2', font= ('verdana', 8, 'bold'))
        self.lb_autorlivro.place(relx=0.002, rely=0.44, relwidth=0.21)

        self.autorlivro_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.veau)
        self.autorlivro_entry.place(relx=0.18, rely=0.43, relwidth=0.27, relheight=0.07)

        # LABEL E ENTRY DO ANO DE PUBLICAÇÃO DO LIVRO
        self.lb_anopubli = Label(self.frame_3, text= 'Ano de Publicaçào do Livro', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_anopubli.place(relx=0.02, rely=0.52, relwidth=0.27, relheight=0.07)

        self.anopubli_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.veca)
        self.anopubli_entry.place(relx=0.31, rely=0.52,relwidth=0.06, relheight=0.07)

        #LABEL E ENTRY DA QUANTIDADE DE LIVROS
        self.lb_qtdlivro = Label(self.frame_3, text= 'Quantidade Disponível', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_qtdlivro.place(relx=0.46, rely=0.52, relwidth=0.23, relheight=0.07)

        self.qtdlivro_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.vecq)
        self.qtdlivro_entry.place(relx=0.71,rely=0.52, relwidth=0.06, relheight=0.07)

    # CRIANDO A LISTA DE LIVROS NO FRAME 4.
    def lista_livros_frame_4(self):
        self.listaLivros = ttk.Treeview(self.frame_4, height= 3, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaLivros.heading('#0', text='')
        self.listaLivros.heading('#1', text='ID')
        self.listaLivros.heading('#2', text='Título do Livro')
        self.listaLivros.heading('#3', text='Autor do Livro')
        self.listaLivros.heading('#4', text='Ano Pubicação')
        self.listaLivros.heading('#5', text='Qtd Disponivel')

        self.listaLivros.column('#0', width=1)
        self.listaLivros.column('#1', width=1)
        self.listaLivros.column('#2', width=200)
        self.listaLivros.column('#3', width=200)
        self.listaLivros.column('#4', width=48)
        self.listaLivros.column('#5', width=48)

        self.listaLivros.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.89)

        self.scroolLista = Scrollbar(self.frame_2, orient= 'vertical')
        self.listaLivros.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.05, relwidth= 0.031, relheight=0.89)
        self.listaLivros.bind('<Double-1>', self.Clique_Duplo)

    # CRIAÇÃO DA FUNÇÃO DE CHECAGEM PARA AS ENTRYS        
    def checkEntrys(self):
        self.vcmd1 = (self.janela.register(self.validate_entrycod), "%P")
        self.vcmd2 = (self.janela.register(self.validate_entry_telefone), '%P')
        self.vcmd3 = (self.janela.register(self.validate_entry_nome), '%P')
        self.vcmd4 = (self.janela.register(self.validate_entry_cidade), '%P')
        self.vecc = (self.janela.register(self.valida_entryidbook), "%P") #vecc = Valida Entrada Campo Codigo.
        self.veca = (self.janela.register(self.validate_entryanopubli), '%P') #veca = Valida Entrada Campo Ano de Publicação.
        self.vecq = (self.janela.register(self.validate_entryqtdlivro), '%P') #vecq = Valida Entrada Campo Qtd Disponiveis.
        self.vect = (self.janela.register(self.validate_entry_titulolivro), '%P') #vect = Valida Entrada Campo Titulo do Livro.
        self.veau = (self.janela.register(self.validate_entry_nameautor), '%P') #veau = Valida Entrada Campo Autor do Livro

    # CRIANDO FRAME DE MENU.
    def Menu(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label = 'Opções', menu= filemenu)
        menubar.add_cascade(label = 'Inventario da Biblioteca', menu= filemenu2)

        filemenu.add_command(label = 'Ficha Simples do Usúario',command= self.gerarRelatCliente) 
        filemenu.add_command(label = 'Ficha Simples do Livro',command=self.gerarRelatLivro)
        filemenu.add_command(label = 'Sair', command= Quit)

        filemenu2.add_command(label='Inventario Geral da Biblioteca', command=self.geraRelatINVENTARIO_LIVROS)
        filemenu2.add_command(label='Relatorio Geral dos Clientes',command= self.geraRelatINVENTARIO_CLIENTES) 

    # CONFIRMANDO O EMPRESTIMO.
    def confirmar_emprestimo_gui(self):
        self.conecta_bd()
    # Obtenha os valores dos campos de entrada
        self.variaveis_Empres_Devol()
    # Chama a função confirmar_emprestimo com os valores dos campos de entrada com os argumentos.
        self.confirmar_emprestimo(self.qtdretirada, self.nomedocliente, self.titulodolivro, self.contatocliente, self.dataretirada)

App_Biblioteca()