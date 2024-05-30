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

# CRIANDO A CLASSE DE VALIDADORES PARA JANELA 1 "CADASTRO DE USUARIOS".
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
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 50:
                return True
            else:
                return False
    
    # VALIDANDO A ENTRY CIDADE.
    def validate_entry_cidade(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 29:
                return True
            else:
                return False

# CRIANDO A CLASSE DE VALIDADORES PARA A JANELA 2 'SISTEMA DA BIBLIOTECA'
class Valida_Win2:
    # CRIANDO OS VALIDORES REFERENTE AS ENTRYS QUE UTILIZAM NÚMEROS, CODIGO DO LIVRO, ANO DE PUBLICAÇÃO E QUANTIDADE DISPONIVEL.
    # FUNÇÃO REFERENTE AO CAMPO CODIGO DO LIVRO.
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
        return 0 <= value <= 10000
    
    # CRIANDO OS VALIDADORES REFERENTE AS ENTRYS QUE UTILIZAM TEXTO, TITULO DO LIVRO, NOME DO AUTOR.
    # FUNÇÃO REFERENTE AO CAMPO TITULO DO LIVRO.
    def validate_entry_titulolivro(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 45:
                return True
            else:
                return False
            
    # FUNÇÃO REFERENTE AO CAMPO DE QUANTIDADE DE LIVROS.
    def validate_entry_nameautor(self, texto):
        if texto == '': return True
        else:
            if all(char.isalpha() or char.isspace() for char in texto) and len(texto) <= 25:
                return True
            else:
                return False

class Relatorios():
    # CRIANDO UMA FUNÇÃO QUE IRA ABRI O NAVEGADOR PADRÃO DO COMPUTADOR.
    def printUsuario(self):
        webbrowser.open('usuario.pdf')

    # CRIANDO UMA FUNÇÃO QUE IRA GERAR OS RELATORIOS BASEADOS NAS ENTRYS.    
    def gerarRelatUsuario(self):
        self.c = canvas.Canvas('usuario.pdf')

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(200, 790, 'Ficha do Usúario')

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
        self.printUsuario()

class Funcs():
    # FUNÇÃO QUE LIMPA TODOS OS CAMPOS.
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    # FUNÇÃO QUE CONECTA O BANCO DE DADOS.
    def conecta_bd(self):
        self.conn = sqlite3.connect('Clientes.bd')
        self.cursor = self.conn.cursor(); print('Conectando ao Banco de Dados de Clientes.')

    # FUNÇÃO QUE DESCONECTA O BANDO DE DADOS.
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando do Banco de Dados dos Clientes.')

    # FUNÇÃO QUE IRA CRIAR A TABELA DE USUARIOS DA BIBLIOTECA.
    def montarTabela(self):
        self.conecta_bd()
        # CRIAR A TABELA
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                cod INTEGER PRIMARY KEY,
                nome_usuario CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit(); print('Banco de Dados Usúarios criado.')
        self.desconecta_bd()

    # CRIANDO UMA FUNÇÃO PARA ABRIGAR VARIAVEIS FACILITANDO PARA QUANDO FOR UTILIZAR POSTERIORMENTE.
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    # FUNÇÃO QUE IRA ADICIONAR USUARIOS.
    def add_usuarios(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO usuarios (nome_usuario, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.seleciona_lista()
        self.limpa_tela()

    # SELECIONANDO A LISTA PARA ADICIONAR AS INFORMAÇÕES.    
    def seleciona_lista(self):
        self.listaCliente.delete(*self.listaCliente.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_usuario, telefone, cidade FROM usuarios
            ORDER BY nome_usuario ASC; """)
        for i in lista:
            self.listaCliente.insert('', END, values=i)
        self.desconecta_bd()

    # FUNÇÃO RESPONSAVEL POR SELECIONAR USUARIOS NA LISTA DO FRAME 2
    def Double_click(self, event):
        self.limpa_tela()
        self.listaCliente.selection()

        for n in self.listaCliente.selection():
            col1, col2, col3, col4 = self.listaCliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    # CRIANDO UMA FUNÇÃO QUE IRA ATUALIZAR O CAMPO CODIGO. EX: USUARIO 2 É EXCLUIDO O USUARIO 3 OS QUE OS SUCEDEREM DEVEM 'SUBIR' NA LISTA
    def atualizar_codigos_usuarios(self):
        self.variaveis()
        self.conecta_bd()
        usuarios = self.cursor.execute("SELECT cod FROM usuarios ORDER BY cod").fetchall()
        for i, usuario in enumerate(usuarios, start=1):
            self.cursor.execute('UPDATE usuarios SET cod = ? WHERE cod = ?',(i, usuario[0]))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.seleciona_lista()

    # CRIANDO A FUNÇÃO DO BOTÃO DELETAR
    def deleta_usuario(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM usuarios WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.atualizar_codigos_usuarios()
        self.limpa_tela()
        self.seleciona_lista()

    # Criando A FUNÇÃO DO BOTÃO ALTERAR.
    def altera_usuario(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE usuarios SET nome_usuario = ?, telefone = ?, cidade = ?
            WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.seleciona_lista()
        self.limpa_tela()

    # CRIANDO A FUNÇÀO DO BOTÀO BUSCAR.
    def busca_usuario(self):
        self.conecta_bd()
        self.listaCliente.delete(*self.listaCliente.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        if nome == '':
            nome = '%'
        self.cursor.execute(
            """ SELECT cod, nome_usuario, telefone, cidade FROM usuarios
            WHERE nome_usuario LIKE '%s' ORDER BY nome_usuario ASC""" % nome)
        buscanomeUsuario = self.cursor.fetchall()
        for i in buscanomeUsuario:
            self.listaCliente.insert('', END, values=i)            
        self.limpa_tela()
        self.desconecta_bd()

class Aplicacao(Funcs, Relatorios, Validadores, Valida_Win2):
    def __init__(self):
        self.janela = janela
        self.validaEntradas()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.lista_frame2()
        self.montarTabela()
        self.seleciona_lista()
        self.Menu()
        janela.mainloop()

    # configurações da janela 1
    def tela(self):
        self.janela.title('Sistema Integrado da Biblioteca')
        self.janela.configure(background= '#1e3743')
        self.janela.geometry('700x600')
        self.janela.resizable(True, True)
        self.janela.minsize(width=500, height=400)
        self.janela.maxsize(width=900, height=800)

    # CRIANDO OS CAMPOS
    def frames(self):
        self.frame_1 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        self.frame_2 = Frame(self.janela, bd= 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    # CRIANDO BOTÕES
    def widgets_frame1(self):
        # CRIANDO O BOTÃO LIMPAR
        self.bt_limpar = Button(self.frame_1, text='Limpar Campos', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'),command=self.limpa_tela)
        self.bt_limpar.place(relx=0.15, rely=0.1, relwidth=0.17, relheight=0.15)
        # CRIANDO O BOTÃO BUSCAR
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.busca_usuario)
        self.bt_buscar.place(relx=0.33,rely=0.1,relwidth=0.1,relheight=0.15)
        # CRIANDO O BOTÃO NOVO
        self.bt_novo = Button(self.frame_1, text='Novo', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.add_usuarios)
        self.bt_novo.place(relx=0.65,rely=0.1,relwidth=0.1,relheight=0.15)
        # CRIANDO O BOTÃO ALTERAR
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.altera_usuario)
        self.bt_alterar.place(relx=0.76, rely=0.1, relwidth=0.1, relheight=0.15)
        # CRIANDO O BOTÃO APAGAR
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command=self.deleta_usuario)
        self.bt_apagar.place(relx=0.87, rely=0.1, relwidth=0.1, relheight=0.15)

        # CRIANDO As LABELS E ENTRADA(entry) ou input no python DO CODIGO
        # LABEL E ENTRADA DO CAMPO CODIGO.
        self.lb_codigo = Label(self.frame_1, text='Código', bg= '#dfe3ee', fg= '#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        # LABEL E ENTRADA DO CAMPO NOME.
        self.lb_nome = Label(self.frame_1, text='Nome', bg= '#dfe3ee', fg= '#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1, validate= 'key', validatecommand= self.vcmd3)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.55)

        # LABEL E ENTRADA DO CAMPO TELEFONE.
        self.lb_telefone = Label(self.frame_1, text='Telefone com DDD', bg= '#dfe3ee', fg= '#107db2')
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd2)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.22)

        # LABEL E ENTRADA DO CAMPO CIDADE.
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg= '#dfe3ee', fg= '#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1, validate='key', validatecommand= self.vcmd4)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.25)
    
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
        self.listaCliente.bind('<Double-1>', self.Double_click)

    # CRIANDO FRAME DE MENU.
    def Menu(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label = 'Opções', menu= filemenu)
        menubar.add_cascade(label = 'Sistema de Gerenciamento dos Livros', menu= filemenu2)

        filemenu.add_command(label = 'Ficha do Usúario', command= self.gerarRelatUsuario)
        filemenu.add_command(label = 'Limpa Usúario', command= self.limpa_tela)
        filemenu.add_command(label = 'Sair', command= Quit)

        filemenu2.add_command(label = 'Sistema de Livros', command= self.chamar_janela2)

    # VALIDAÇÃO DAS ENTRADAS.
    def validaEntradas(self):
        self.vcmd1 = (self.janela.register(self.validate_entrycod), "%P")
        self.vcmd2 = (self.janela.register(self.validate_entry_telefone), '%P')
        self.vcmd3 = (self.janela.register(self.validate_entry_nome), '%P')
        self.vcmd4 = (self.janela.register(self.validate_entry_cidade), '%P')

    # CRIAÇÃO DA SEGUNDA JANELA A PARTIR DESTE PONTO SERA APENAS PARA A BIBLIOTECA (LIVROS, AUTORES, QUANTIDADE DE LIVROS, EMPRESTIMO E DEVOLUÇÃO)
    # CHAMANDO A JANELA 2.
    def chamar_janela2(self):
        self.cria_janela2()
        self.checkEntrys()
        self.frames_janela2()
        self.widgets_frame_3()
        self.limpar_campos()
        self.lista_livros_frame_4()
        self.Menu_Window2()

    # CRIANDO E CONFIGURANDO A JANELA 2.
    def cria_janela2(self):
        self.janela2 = Toplevel()
        self.janela2.title('Sistema Integrado da Biblioteca - Emprestimo e Devolução de Livros.')
        self.janela2.configure(background= 'lightblue')
        self.janela2.geometry('700x600')
        self.janela2.resizable(False, False)
        self.janela2.transient(self.janela)
        self.janela2.focus_force()
        self.janela2.grab_set()
    
    # CRIANDO FRAMES DA JANELA 2.
    def frames_janela2(self):
        self.frame_3 = Frame(self.janela2, background= 'red')
        self.frame_3.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_4 = Frame(self.janela2, background= 'red')
        self.frame_4.place(relx=0.02, rely=0.52, relwidth=0.96, relheight=0.46)

    # ADICIONANDO A FUNÇÃO DE LIMPAR TODOS OS CAMPOS DA BIBLIOTECA.
    def limpar_campos(self):
        self.idbook_entry.delete(0, END)
        self.nomelivro_entry.delete(0, END)
        self.autorlivro_entry.delete(0, END)
        self.anopubli_entry.delete(0, END)
        self.qtdlivro_entry.delete(0, END)

    # CRIANDO WIDGETS PARA O FRAME 3.
    def widgets_frame_3(self):
        # CRIANDO BOTÕES DE CADASTRO DO LIVRO, BUSCAR LIVRO, DEVOLUÇÃO, EMPRESTIMO.
        self.bt_newbook = Button(self.frame_3, text= 'Confirmar Cadastro do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'))
        self.bt_newbook.place(relx=0.02, rely=0.85, relwidth=0.29, relheight=0.12)

        self.bt_buscalivro = Button(self.frame_3, text= 'Buscar Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'))
        self.bt_buscalivro.place(relx=0.33, rely=0.85, relwidth=0.14, relheight=0.12)

        self.bt_emprestimo = Button(self.frame_3, text= 'Emprestimo do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'))
        self.bt_emprestimo.place(relx=0.56, rely=0.85, relwidth=0.21, relheight=0.12)

        self.bt_devolucao = Button(self.frame_3, text= 'Devolução do Livro', bd=2, bg='#107db2', fg= 'white', font= ('verdana', 8, 'bold'))
        self.bt_devolucao.place(relx=0.78, rely=0.85, relwidth=0.2, relheight=0.12)

        # CRIANDO AS LABELS E AS ENTRYS DO FRAME 3.
        self.lb_idbook = Label(self.frame_3, text= 'ID do Livro', bg= '#87CEEB', fg='#191970', font=('verdana', 8, 'bold'))
        self.lb_idbook.place(relx=0.02, rely=0.05, relwidth=0.16, relheight=0.07)

        self.idbook_entry = Entry(self.frame_3, validate='key', validatecommand= self.vecc)
        self.idbook_entry.place(relx=0.19, rely=0.05, relwidth=0.07)

        # CRIANDO LABEL E ENTRY DO CADASTRO DO LIVRO
        self.lb_newbook = Label(self.frame_3, text= 'Informaçòes do Livro', bg='#87ceeb', fg='#191970', font= ('verdana', 8, 'bold'))
        self.lb_newbook.place(relx=0.39, rely=0.21, relwidth=0.22)

        self.lb_nomelivro = Label(self. frame_3, text='Título do Livro', bg='#87cceb', fg='#191970', font=('verdana', 8, 'bold'))
        self.lb_nomelivro.place(relx=0.02, rely=0.32, relwidth=0.16, relheight=0.07)

        self.nomelivro_entry = Entry(self.frame_3, validate= 'key', validatecommand=self.vect)
        self.nomelivro_entry.place(relx=0.2, rely=0.32, relwidth=0.47, relheight=0.07)

        # CRIANDO A LABEL E A ENTRY DO NOME DO AUTOR.
        self.lb_autorlivro = Label(self.frame_3, text= 'Autor do Livro', bg='#97cceb', fg='#191970', font= ('verdana', 8, 'bold'))
        self.lb_autorlivro.place(relx=0.02, rely=0.42, relwidth=0.21)

        self.autorlivro_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.veau)
        self.autorlivro_entry.place(relx=0.25, rely=0.42, relwidth=0.27, relheight=0.07)

        # LABEL E ENTRY DO ANO DE PUBLICAÇÃO DO LIVRO
        self.lb_anopubli = Label(self.frame_3, text= 'Ano de Publicaçào do Livro', bg='#97cceb', fg='#191970', font=('verdana', 8, 'bold'))
        self.lb_anopubli.place(relx=0.02, rely=0.52, relwidth=0.27, relheight=0.07)

        self.anopubli_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.veca)
        self.anopubli_entry.place(relx=0.31, rely=0.52,relwidth=0.06, relheight=0.07)

        #LABEL E ENTRY DA QUANTIDADE DE LIVROS
        self.lb_qtdlivro = Label(self.frame_3, text= 'Quantidade Disponível', bg='#97cceb', fg='#191970', font=('verdana', 8, 'bold'))
        self.lb_qtdlivro.place(relx=0.46, rely=0.52, relwidth=0.23, relheight=0.07)

        self.qtdlivro_entry = Entry(self.frame_3, validate= 'key', validatecommand= self.vecq)
        self.qtdlivro_entry.place(relx=0.71,rely=0.52, relwidth=0.06, relheight=0.07)

    # CRIANDO A LISTA DE LIVROS NO FRAME 4.
    def lista_livros_frame_4(self):
        self.listaLivros = ttk.Treeview(self.frame_4, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.listaLivros.heading('#0', text='ID')
        self.listaLivros.heading('#1', text='Nome do Livro')
        self.listaLivros.heading('#2', text='Autor do Livro')
        self.listaLivros.heading('#3', text='Ano de Publicação')
        self.listaLivros.heading('#4', text='Qtd Disponíveis')

        self.listaLivros.column('#0', width=1)
        self.listaLivros.column('#1', width=100)
        self.listaLivros.column('#2', width=100)
        self.listaLivros.column('#3', width=70)
        self.listaLivros.column('#4', width=70)

        self.listaLivros.place(relx=0.00, rely=0.00, relwidth=1, relheight=0.07)

    # CRIANDO O MENU PARA A JANELA 2.
    def Menu_Window2(self):
        barramenu = Menu(self.janela2)
        self.janela2.config(menu=barramenu)
        firstmenu = Menu(barramenu)
        

        def Quit(): self.janela2.destroy()

        barramenu.add_cascade(label= 'Opçòes', menu= firstmenu)
        firstmenu.add_command(label= 'Limpar Campos', command= self.limpar_campos)
        firstmenu.add_command(label= 'Gerar Relatorio Detalhado')
        firstmenu.add_command(label= 'Sair', command= Quit)

    # CRIANDO A FUNÇÃO DE VALIDAR AS ENTRYS: O OBJETIVO É NÃO PERMITIR A DIGITAÇÃO DE MUMEROS NO CAMPO DE TEXTO E VICE VERSA.
    def checkEntrys(self):
        self.vecc = (self.janela2.register(self.valida_entryidbook), "%P") #vecc = Valida Entrada Campo Codigo.
        self.veca = (self.janela2.register(self.validate_entryanopubli), '%P') #veca = Valida Entrada Campo Ano de Publicação.
        self.vecq = (self.janela2.register(self.validate_entryqtdlivro), '%P') #vecq = Valida Entrada Campo Qtd Disponiveis.
        self.vect = (self.janela2.register(self.validate_entry_titulolivro), '%P') #vect = Valida Entrada Campo Titulo do Livro.
        self.veau = (self.janela2.register(self.validate_entry_nameautor), '%P') #veau = Valida Entrada Campo Autor do Livro

Aplicacao()