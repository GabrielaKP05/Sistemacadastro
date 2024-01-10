from tkinter import messagebox
import mysql.connector
from tkinter import *
from tkinter import ttk
import xlsxwriter  

#conectar ao banco de dados MYSQL
cnx = mysql.connector.connect(
    host = '127.0.0.1',
    user='root',
    password='',
)

#executar a instrução SQL para verificar se o banco de dados existe
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "agenda"')

#obter o numero de resultados 
num_results = cursor.fetchone()[0]

#fechar a conexão com o banco de dados
cnx.close()

#se o número de resultados for maior que zero, o banco de dados existe
if num_results > 0:
 print('O banco de dados agenda existe e esta pronto para uso.')
else:
    #conectar-se ao servidor MySQL para criar o banco de dados
    cnx = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
)
   #criar o banco de dados agenda
    cursor = cnx.cursor()
    cursor.execute('CREATE DATABASE agenda')
    cnx.commit()
    
    #conectar-se ao banco de dados agenda recém-criado
    cnx = mysql.connector.connect(
    host =  '127.0.0.1',
    user = 'root',
    password = '',
    database = 'agenda', #especificar o banco de dados/sempre informar database
)
    # criar a tabela contatos
    cursor = cnx.cursor()
    cursor.execute('CREATE TABLE contatos(id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255),telefone VARCHAR(255))')#id sempre inteiro(inteiro= 1 a 12 caracteres)
    

    cursor.execute("""
    CREATE TABLE grupos(
        id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255)
        )
    """)
    #fechar a conexão com banco de dados
    cnx.commit()
    cnx.close()

class CrudApp:
 

   def __init__(self, window):
    self.window = window
    self.window.title('CRUD usando Python e MySQL')


    self.db = mysql.connector.connect(
      host =  '127.0.0.1',
      user = 'root',
      password = '',
      database = 'agenda',
    )

    #criar a tabela treeview
    #as colunas da tabela são definidas usando o argumento colums no construtor
    self.table = ttk.Treeview(self.window, columns=('ID','Nome','Telefone','Email'),show='headings')
    #definido o cabeçalho de cada coluna é definido usando o metodo heading
    self.table.heading('ID',text='ID')
    self.table.heading('Nome',text='Nome')
    self.table.heading('Telefone',text='Telefone')
    self.table.heading('Email',text='Email')
    #adicionando a tabela na janela
    #a tabela é adicionada na janela do aplicativo 
    self.table.pack(fill=BOTH,expand=True)

    #botão para adicionar
    self.add_btn = Button(self.window,text='Adicionar Contato',command=self.add_data_window)
    self.add_btn.pack()

    #botões para atualizar e deletar
    self.update_btn= Button(self.window,text='Atualizar',command=self.update_data_window)
    self.update_btn.pack()

    self.delete_btn=Button(self.window,text='Deletar',command=self.delete_data)
    self.delete_btn.pack()

    report_btn=Button(self.window,text='Gerar relatório',command=self.generate_report)
    report_btn.pack()

    self.add_grupo_btn= Button(self.window,text='Adicionar grupo',command=self.add_data_grupo_window)
    self.add_data_grupo_btn.pack()

    #alinhar botões
    self.butttons = [self.add_btn, self.update_btn, self.delete_btn, report_btn, self.add_grupo_btn]
    self.align_buttons


    #atualizar a tabela inicialmente

    self.fetch_data()


def align_buttons(self):
    for button in self.buttons:
        button.pack(side=LEFT)
        #posicionar os potões na horizontal

def generate_report(self):
    #obter os dados da tabela

    cursor=self.db.cursor()
    cursor.execute('SELECT * FROM contatos')
    data=[]
    for row in cursor.fetchall():
        data.append(row)


        #criar um objeto de planilha do excel
        workbook = xlsxwriter.Workbook('contatos.xlsx')
        worksheet = workbook.add_worksheet()

        #definir o cabeçalho da planilha
        worksheet.write('A1','ID')
        worksheet.write('B1','Nome')
        worksheet.write('C1','Telefone')
        worksheet.write('D1','Email')

        #escrever os dados da tabela na planilha
        for i, row in enumerate(data):
              worksheet.write(i + 1, 0, row[0])
              worksheet.write(i + 1, 1, row[1])
              worksheet.write(i + 1, 2, row[2])
              worksheet.write(i + 1, 3, row[3])
        #Salvar a planilha
    workbook.close()


    # Exibir uma mensagem de confirmação
    messagebox.showinfo('Sucesso', 'Relatório gerado com sucesso!')

    def fetch_data(self):
        #Buscar dados do banco de dados e popular a tabela treeview
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM contatos')
        rows = cursor.fetchall()

        #limpar dados anteriores
        for row in self.table.get_children():
            self.table.delete(row)

        #adicionar novos dados
        for row in rows:
            self.table.insert('', 'end', values=row)

        #adicionar umj evento de seleção
        self.table.bind('<<TreeViewSelect>>', self.on_select)

    def on_select(self, event):
        #obter o item selecionado
        item = self.table.selction()[0]

        data=self.table.item(item,'values')
        id = data[0]
        nome = data[1]
        telefone = data[2]
        email = data[3]
        #fazer algo com os dados

    def add_data_window(self):
        #janela para adicionar dados
        #cria uma nova janela chamada add_window como filha da janela principal
        #configura a nova janela para que sua origem esteja no canto superior esquerdo da janela principal

        add_window - Toplevel(self.window)
        add_window.tittle('Adicionar contato')

        #entradas para adicionar dados
        nome_label = Label(add_window, text='Nome: ')
        nome_label.grid(row=0, column=0, padx=10, pady=10)
        nome_entry=Entry(add_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        telefone_label = Label(add_window, text='Telefone: ')
        telefone_label.grid(row=1, column=0, padx=10, pady=10)
        telefone_entry=Entry(add_window)
        telefone_entry.grid(row=1, column=1, padx=10, pady=10)

        email_label = Label(add_window, text='Telefone: ')
        email_label.grid(row=2, column=0, padx=10, pady=10)
        email_entry=Entry(add_window)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        #botao para confirmar ação
        confirm_btn=Button(add_window, text='Adicionar', command=lambda: self.add_data(nome_entry.get(), telefone_entry.get(), email_entry.get(), add_window))
        confirm_btn.grid(row=3,column=0, columnspan=2, pady=10)

        def add_data_grupo_window(self):
        #janela para adicionar dados
        #cria uma nova janela chamada add_window como filha da janela principal

        #configura a nova janela para que sua origem esteja no canto superir esquerdo da janela principal
         add_window = Toplevel(self.window)
         add_window.title('Adicionar grupo')


        #entradas para adicionar dados
         nome_label=Label(add_window, text='Nome do grupo:')
         nome_label.grid(row=0, column=0, padx=10, pady=10)
         nome_entry=Entry(add_window)
         nome_entry.grid(row=0, column=1, padx=10, pady=10)

        #botao para confirmar adição
        confirm_btn=Button(add_window, text='Adicionar', command=lambda: self.add_data_grupo(nome_entry.get(), add_window))
        confirm_btn.grid(row=3,column=0, columnspan=2, pady=10)

    def add_data_grupo(self,nome, add_window):
        #validar o nome do grupo
        if nome=='':
            messagebox.showerror('Erro', 'O nome do grupo não pode estar vazio.')
            return

        #adicionar dados no banco de dados
        cursor=self.db.cursor()
        cursor.execute('INSERT INTO grupos(nome) VALUES (%s)', (nome,))
        self.db.commit()
        add_window.destroy()
        self.fetch_data()


    def add_data(self,nome,telefone,email, add_window):
            #adicionar dados no banco de dados
        cursor=self.db.cursor()
        cursor.execute('INSERT INTO contatos(nome, telefone,email) VALUES (%s,%s,%s)', (nome,telefone,email))
        self.db.commit()
        add_window.destroy()
        self.fetch_data()

    def update_data_window(self):
        #janela para atualizar dados
        update_window = Toplevel(self.window)
        update_window.tittle('Atualizar contato')


        nome_label = Label(update_window, text='Novo Nome: ')
        nome_label.grid(row=1, column=0, padx=10, pady=10)
        nome_entry=Entry(update_window)
        nome_entry.grid(row=1, column=1, padx=10, pady=10)

        telefone_label = Label(update_window, text='Novo Telefone: ')
        telefone_label.grid(row=2, column=0, padx=10, pady=10)
        telefone_entry=Entry(update_window)
        telefone_entry.grid(row=2, column=1, padx=10, pady=10)

        email_label = Label(update_window, text=' Novo Telefone: ')
        email_label.grid(row=3, column=0, padx=10, pady=10)
        email_entry=Entry(update_window)
        email_entry.grid(row=3, column=1, padx=10, pady=10)


#botao para confirear atualizacao e a função self.update_data é chamada quando o botão é pressionado.Esta funcao atualiza os dados do usuario con base nas informacoes inseridas nos campos de entrada (Entry) -*Os argumentos da função self.update data são os valores obtidos dos campos de entrada, bem como a janela update window.No executar este código, um botão chanado 'Atualizar" será exibido na janela. Quando o botão é pressionado, a função self.update data será chamada, informações inseridas

        confirm_btn = Button(update_window, text='Atualizar', command=lambda: self.update_data(nome_entry.get(), telefone_entry.get(), email_entry.get(), update_window))
        confirm_btn.grid(row=4, column=0, colspan=2, pady=10)

    def update_data(self, novo_nome, novo_telefone, novo_email, update_window):
        item = self.table.selection()[0]
        data = self. table.item(item, 'values')
        id = data[0]
        # Atualizar dados no banco de dados

        # o objeto 'cursor' é utilizado para executar a instrução soL

        cursor = self.db.cursor()
        cursor. execute('UPDATE contatos SET nome%s, telefone=%s, email=%sWHERE id=%s', (novo_nome, novo_telefone, novo_email, id))

        # Confirma a alteração no banco de dados usando a função commit self.db.commit()

      

        self.db.commit()
      
        # Fecha a janela de atualização update window.destroy()

        update_window.destroy()
     #recupera os dados atualizados da tabela 'contatos' usando a função 'fetch_data'
        self.fetch_data()

    def delete_data(self):
        #obter o item selecionado
        item= self.table.selection()[0]
        #pegar o ID do contato selecionado 
        data= self.table.item(item,'values')
        id= data[0]

        #verificar se o usuario realmente deseja excluir o registro
    if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o registro?'):
        #deletar dados do banco de dados
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM contatos WHERE id=%s', (id,))
        #passe o ID como uma tupla de um elemento
        self.db.commit()
        self.fetch_data()

if __name__=="main"  :
    window=Tk()
    app=CrudApp(window) 
    window.mainloop()     

    

       




  



  










