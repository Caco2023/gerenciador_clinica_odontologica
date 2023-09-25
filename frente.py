from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import conexao
import tkinter.font as tkFont

app = Tk()
app.title("Orthovida - Consultório Odontológico")
app.geometry("1200x600")

ABAS = ttk.Notebook(app)
ABAS.place(x=0, y=0, width=1200, height=600)

#Aba agenda

AGENDA = Frame(ABAS)
ABAS.add(AGENDA, text="Agenda")

######################################## Função para criar nova tabela ########################################

def criarNovaTabela():
    vquery = "CREATE TABLE '"+CONFERENCIA_ENT.get()+"' (HORARIOS VARCHAR(7), NOME VARCHAR(50), TELEFONE VARCHAR(15));"
    conexao.dml(vquery)
    vquery_1 = "INSERT INTO '"+CONFERENCIA_ENT.get()+"' (HORARIOS) VALUES ('08:00'), ('08:30'), ('09:00'), ('09:30'), ('10:00'), ('10:30'), ('11:00'), ('11:30'), ('14:00'), ('14:30'), ('15:00'), ('15:30'), ('16:00'), ('16:30'), ('17:00'), ('17:30'), ('18:00'), ('18:30'), ('19:00'), ('19:30')"            
    conexao.dml(vquery_1)
    
######################################## Ciaxa de inserção de dados ###########################################
def inserirPaciente():
    vNOME = NOME_ENT.get().upper()
    vTELEFONE = TELEFONE_ENT.get()
    vHORARIO = BOTAO_HORARIOS.get()
    
    if vNOME == "":
        messagebox.showinfo(title="ATENÇÃO", message="Digite um Nome!")
    
    elif vTELEFONE == "":
        messagebox.showinfo(title="ATENÇÃO", message="Digite um Número de Telefone!")
    
    elif vHORARIO == "":
        messagebox.showinfo(title="ATENÇÃO", message="Selecione um horário!")
                
    else:
        vquery = "UPDATE '"+VISOR_DATA_TEXTO.get()+"' SET NOME='"+vNOME+"', TELEFONE='"+vTELEFONE+"' WHERE HORARIOS='"+vHORARIO+"'"
        conexao.dml(vquery)   
        NOME_ENT.delete(0, END)   
        TELEFONE_ENT.delete(0, END)   
        BOTAO_HORARIOS.delete(0, END)           
        mostrarNaAgenda()
    
    
def mostrarNaAgenda():
    try:
        TELA.delete(*TELA.get_children())    
        vquery = "SELECT HORARIOS, NOME,TELEFONE FROM '"+VISOR_DATA_TEXTO.get()+"'"
        linhas = conexao.dql(vquery)
        for i in linhas:
            TELA.insert("", "end", values=i)
    except:
        res = messagebox.askquestion(title="Data não existente!", message="Gostaria de cirar agenda para essa data?")
        if res == "yes":
            criarNovaTabela()
            TELA.delete(*TELA.get_children())    
            vquery = "SELECT HORARIOS, NOME,TELEFONE FROM '"+CONFERENCIA_ENT.get()+"'"
            linhas = conexao.dql(vquery)
            for i in linhas:
                TELA.insert("", "end", values=i)
                
            
def funcaoBotaoConfirmarPciente():
    def botaoConfirmarProcedimento():
        vquery = "INSERT INTO procedimentos (DATA, NOME, PROCEDIMENTO, DENTE, FACE, VALOR) VALUES ('"+VISOR_DATA_TEXTO.get()+"', '"+ENT_PACIENTE.get()+"', '"+COMB_PROCEDIMENTOS.get()+"', '"+COMB_DENTE.get()+"', '"+COMB_FACE.get()+"', '"+ENT_VALOR.get()+"')"
        conexao.dml(vquery)   
        JANELA_PROCEDIMENTOS.destroy()
    try:
        TELA_TEXTO = TELA.selection()[0]   
        TELA_TEXTO_1 = TELA.item(TELA_TEXTO, "values")          
        
        JANELA_PROCEDIMENTOS = Tk()
        JANELA_PROCEDIMENTOS.title("Selecione o Procedimento")
        JANELA_PROCEDIMENTOS.geometry("400x350")
        L_PACIENTE = Label(JANELA_PROCEDIMENTOS, text="Paciente")
        L_PACIENTE.place(x=20, y=20)
        ENT_PACIENTE = Entry(JANELA_PROCEDIMENTOS)
        ENT_PACIENTE.place(x=20, y=40, width=360)
        ENT_PACIENTE.insert(END, TELA_TEXTO_1[1])
        L_PROCEDIMENTOS = Label(JANELA_PROCEDIMENTOS, text="Selecione um procedimento")
        L_PROCEDIMENTOS.place(x=20, y=70)
        COMB_PROCEDIMENTOS = ttk.Combobox(JANELA_PROCEDIMENTOS, values=LISTA_PROCEDIMENTOS)
        COMB_PROCEDIMENTOS.place(x=20, y=90, width=360)
        L_DENTE = Label(JANELA_PROCEDIMENTOS, text="Selecione o dente")
        L_DENTE.place(x=20, y=120)
        COMB_DENTE = ttk.Combobox(JANELA_PROCEDIMENTOS, values=NUMERO_DOS_DENTES)
        COMB_DENTE.place(x=20, y=140)
        L_FACE = Label(JANELA_PROCEDIMENTOS, text="Selecione a facce do dente")
        L_FACE.place(x=200, y=120)
        COMB_FACE = ttk.Combobox(JANELA_PROCEDIMENTOS, values=FACES_DOS_DENTES)
        COMB_FACE.place(x=200, y=140, width=160)
        L_VALOR = Label(JANELA_PROCEDIMENTOS, text="Valor pago")
        L_VALOR.place(x=20, y=170)
        L_CIFRAO = Label(JANELA_PROCEDIMENTOS, text="R$:")
        L_CIFRAO.place(x=20, y=200)
        ENT_VALOR = Entry(JANELA_PROCEDIMENTOS)
        ENT_VALOR.place(x=40, y=200)
        BOTAO_CONFIRMAR_PROCEDIMENTO = Button(JANELA_PROCEDIMENTOS, text="Confirmar", command=botaoConfirmarProcedimento)
        BOTAO_CONFIRMAR_PROCEDIMENTO.place(x=20, y=250, width=360)
    except:
        messagebox.showinfo(title="ATENÇÃO", message="Selecione um paciente da agenda")
        return    

def funcaoBotaoDesmarcarPaciente():
    
    def deletarPaciente():
        vquery = "UPDATE '"+VISOR_DATA_TEXTO.get()+"' SET NOME='None', TELEFONE='None' WHERE NOME='"+ENT_NOME_PACIENTE.get()+"'" 
        conexao.dml(vquery)
    def botaoRemarcacaoPaciente():
        VAR_DATA = COMB_DIA.get()+"/"+COMB_MES.get()+"/"+COMB_ANO.get()        
        if ENT_NOME_PACIENTE == "":
            messagebox.showinfo(title="ATENÇÃO", message="Digite um Nome!")
    
        elif ENT_TELEFONE_PACIENTE == "":
            messagebox.showinfo(title="ATENÇÃO", message="Digite um Número de Telefone!")
    
        elif COMB_HORARIO == "":
            messagebox.showinfo(title="ATENÇÃO", message="Selecione um horário!")
            
        elif COMB_DIA == "":
            messagebox.showinfo(title="ATENÇÃO", message="Selecione um dia!")
                
        elif COMB_MES == "":
            messagebox.showinfo(title="ATENÇÃO", message="Selecione um mês!")
            
        elif COMB_ANO == "":
            messagebox.showinfo(title="ATENÇÃO", message="Selecione um ano!")
                
        else:
            try:
                deletarPaciente() 
                vquery = "UPDATE '"+VAR_DATA+"' SET NOME='"+ENT_NOME_PACIENTE.get()+"', TELEFONE='"+ENT_TELEFONE_PACIENTE.get()+"' WHERE HORARIOS='"+COMB_HORARIO.get()+"'"
                conexao.dml(vquery)          
                mostrarNaAgenda()
                JANELA_REMARCACAO.destroy()
            except:
                PERGUNTA = messagebox.askquestion(title="ATENÇÃO", message="A data selecionada não existe. Gostaria de criar uma agenda para essa data?")
                if PERGUNTA == "yes":
                    deletarPaciente()
                    vquery = "CREATE TABLE '"+VAR_DATA+"' (HORARIOS VARCHAR(7), NOME VARCHAR(50), TELEFONE VARCHAR(15));"
                    conexao.dml(vquery)
                    vquery_1 = "INSERT INTO '"+VAR_DATA+"' (HORARIOS) VALUES ('08:00'), ('08:30'), ('09:00'), ('09:30'), ('10:00'), ('10:30'), ('11:00'), ('11:30'), ('14:00'), ('14:30'), ('15:00'), ('15:30'), ('16:00'), ('16:30'), ('17:00'), ('17:30'), ('18:00'), ('18:30'), ('19:00'), ('19:30')"            
                    conexao.dml(vquery_1)
                    vquery_2 = "UPDATE '"+VAR_DATA+"' SET NOME='"+ENT_NOME_PACIENTE.get()+"', TELEFONE='"+ENT_TELEFONE_PACIENTE.get()+"' WHERE HORARIOS='"+COMB_HORARIO.get()+"'"
                    conexao.dml(vquery_2)
                    mostrarNaAgenda()
                    JANELA_REMARCACAO.destroy()
                else:
                    return
         
    res = messagebox.askquestion(title="Paciente não compareceu", message="Deseja remarcar o paciente?")
    if res == "yes":
        try:
            TELA_TEXTO = TELA.selection()[0]   
            TELA_TEXTO_1 = TELA.item(TELA_TEXTO, "values")   
            JANELA_REMARCACAO = Tk()
            JANELA_REMARCACAO.title("Remarcar o paciente")
            JANELA_REMARCACAO.geometry("500x290")
            L_NOME_PACIENTE = Label(JANELA_REMARCACAO, text="Nome")
            L_NOME_PACIENTE.place(x=10, y=10)
            ENT_NOME_PACIENTE = Entry(JANELA_REMARCACAO)
            ENT_NOME_PACIENTE.place(x=10, y=30, width=480)
            ENT_NOME_PACIENTE.insert(END, TELA_TEXTO_1[1])
            L_TELEFONE_PACIENTE = Label(JANELA_REMARCACAO, text="Telefone")
            L_TELEFONE_PACIENTE.place(x=10, y=60)
            ENT_TELEFONE_PACIENTE = Entry(JANELA_REMARCACAO)
            ENT_TELEFONE_PACIENTE.place(x=10, y=80, width=230)
            ENT_TELEFONE_PACIENTE.insert(END, TELA_TEXTO_1[2])
            L_HORARIO = Label(JANELA_REMARCACAO, text="Horário")
            L_HORARIO.place(x=250, y=60)
            COMB_HORARIO = ttk.Combobox(JANELA_REMARCACAO, values=LISTA_HORARIOS)
            COMB_HORARIO.place(x=250, y=80, width=230)
            L_DIA = Label(JANELA_REMARCACAO, text="Dia")
            L_DIA.place(x=10, y=110)
            L_MES = Label(JANELA_REMARCACAO, text="Mês")
            L_MES.place(x=80, y=110)
            L_ANO = Label(JANELA_REMARCACAO, text="Ano")
            L_ANO.place(x=150, y=110)
            COMB_DIA = ttk.Combobox(JANELA_REMARCACAO, values=LISTA_DIAS)
            COMB_DIA.place(x=10, y=130, width=40)
            COMB_MES = ttk.Combobox(JANELA_REMARCACAO, values=LISTA_MES)
            COMB_MES.place(x=55, y=130, width=80)
            COMB_ANO = ttk.Combobox(JANELA_REMARCACAO, values=LISTA_ANO)
            COMB_ANO.place(x=140, y=130, width=50)
            BOTAO_CONFIRMAR_RAMARCACAO = Button(JANELA_REMARCACAO, text="Comfirma a remacação", command=botaoRemarcacaoPaciente)
            BOTAO_CONFIRMAR_RAMARCACAO.place(x=170, y=220, width=160, height=40)
        except:
            messagebox.showinfo(title="ATENÇÃO", message="Selecione um paciente para remarcar!")
        
    else:
        return
        
        
                     

################################# Area de inderir pacientes######################################################################

INSERIR_DADOS = LabelFrame(AGENDA, text="Inserir Pacientes", borderwidth=1, relief="solid")
INSERIR_DADOS.place(x=10, y=10, width=1180, height=100)

NOME = Label(INSERIR_DADOS, text="Nome")
NOME.place(x=10, y=10)

NOME_ENT = Entry(INSERIR_DADOS)
NOME_ENT.place(x=10, y=35, width=400, height=25)

TELEFONE = Label(INSERIR_DADOS, text="Telefone")
TELEFONE.place(x=425, y=10)

TELEFONE_ENT = Entry(INSERIR_DADOS)
TELEFONE_ENT.place(x=425, y= 35, width=200, height=25)

HORARIOS = Label(INSERIR_DADOS, text="Horarios")
HORARIOS.place(x=640, y=10)

LISTA_HORARIOS = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30"]

BOTAO_HORARIOS = ttk.Combobox(INSERIR_DADOS, values=LISTA_HORARIOS)
BOTAO_HORARIOS.place(x=640, y=35, width=100, height=25)

LISTA_DIAS_INSERIR = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28", "29", "30"]
LISTA_DIAS_1_INSERIR  = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28", "29", "30", "31"]
LISTA_DIAS_FEV_INSERIR = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28"]
LISTA_MES_INSERIR = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
LISTA_ANO_INSERIR = ["2023", "2024", "2025", "2026"]

BOTAO_INSERIR = Button(INSERIR_DADOS, text="Marcar", command=inserirPaciente)
BOTAO_INSERIR.place(x=1000, y=30, width=150, height=30)


##################################### Visor #################################################

VISOR = LabelFrame(AGENDA, text="Agenda", borderwidth=1, relief="solid")
VISOR.place(x=10, y=130, width=1180, height=430)


##################################### Seleção data ##########################################

def inserirData():
    ID_DIA = BOTAO_DIA.get()
    ID_MES = BOTAO_MES.get()
    ID_ANO = BOTAO_ANO.get()
    
    if ID_DIA == "":
        messagebox.showinfo(title="ATENÇÃO", message="Selecione um dia!")
    
    elif ID_MES == "":
        messagebox.showinfo(title="ATENÇÃO", message="Selecione um mes!")
        
    elif ID_ANO == "":
        messagebox.showinfo(title="ATENÇÃO", message="Selecione um ano!")
        
    else:
        ID_DATA = ID_DIA + "/" + ID_MES + "/" +ID_ANO
        CONFERENCIA_ENT.insert(END, ID_DATA)
        

def InserirVisorData():
    VISOR_DATA_TEXTO.delete(0, END)
    VD_DATA = CONFERENCIA_ENT.get()    
    VISOR_DATA_TEXTO.insert(END, VD_DATA)
    mostrarNaAgenda()
    CONFERENCIA_ENT.delete(0,END)
      
    

SELECAO_DATA = LabelFrame(VISOR, text="Data", borderwidth=1, relief="solid")
SELECAO_DATA.place(x=10, y=10, width=200, height=250)

LISTA_DIAS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28", "29", "30"]
LISTA_DIAS_1  = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28", "29", "30", "31"]
LISTA_DIAS_FEV = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26","27", "28"]
LISTA_MES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
LISTA_ANO = ["2023", "2024", "2025", "2026"]

DIA = Label(SELECAO_DATA, text="Dia:")
DIA.place(x=15, y=10)

BOTAO_DIA = ttk.Combobox(SELECAO_DATA, values=LISTA_DIAS)
BOTAO_DIA.place(x=10, y=30, width=40)

MES = Label(SELECAO_DATA, text= "Mês:")
MES.place(x=80, y=10)

BOTAO_MES = ttk.Combobox(SELECAO_DATA, values=LISTA_MES)
BOTAO_MES.place(x=55, y=30, width=80)

ANO = Label(SELECAO_DATA, text="Ano:")
ANO.place(x=150, y=10)

BOTAO_ANO = ttk.Combobox(SELECAO_DATA, values=LISTA_ANO)
BOTAO_ANO.place(x=140, y=30, width=50)

BOTAO_SELECAO = Button(SELECAO_DATA, text="Selecionar", command=inserirData)
BOTAO_SELECAO.place(x=10, y=60, width=180)

CONFERENCIA = Label(SELECAO_DATA, text="Conferir a Data:")
CONFERENCIA.place(x=60, y=110)

CONFERENCIA_ENT = Entry(SELECAO_DATA)
CONFERENCIA_ENT.place(x=10, y=130, width=180, height=25)

BOTAO_CONFIRMAR = Button(SELECAO_DATA, text="Confirmar Data", command=InserirVisorData)
BOTAO_CONFIRMAR.place(x=10, y=180, width=180, height=30)


################################## Visor Data#########################################

VISOR_DATA = LabelFrame(VISOR, text="Data", border=1, relief="solid")
VISOR_DATA.place(x=10, y=270, width=200, height=130)
VISOR_DATA_TEXTO = Entry(VISOR_DATA)
VISOR_DATA_TEXTO_FONT = tkFont.Font(family="arial", size=17, weight="bold")
VISOR_DATA_TEXTO.configure(font=VISOR_DATA_TEXTO_FONT)
VISOR_DATA_TEXTO.place(x=5, y=5, width=190, height=100)


################################### Agenda ###########################################

TELA = ttk.Treeview(VISOR, columns=("HORARIO", "NOME", "TELEFONE"), show="headings", padding=2)
TELA.column("HORARIO", minwidth=0, width=30)
TELA.column("NOME", minwidth=0, width=300)
TELA.column("TELEFONE", minwidth=0, width=100)
TELA.heading("HORARIO", text="HORARIO")
TELA.heading("NOME", text="NOME")
TELA.heading("TELEFONE", text="TELEFONE")
TELA.place(x=220, y=17, width=750, height=383)


################################### BOTOES CONFIRMAR E DESMARCAR #####################

BOTAO_CONFIRMAR_PACIENTE = Button(VISOR, text="Confirmar Paciente", background="green", command=funcaoBotaoConfirmarPciente)
BOTAO_CONFIRMAR_PACIENTE.place(x=1000, y= 150, width=150, height=50)

BOTAO_REMARCAR_PACIENTE = Button(VISOR, text="Remarcar Paciente", background="red", command=funcaoBotaoDesmarcarPaciente)
BOTAO_REMARCAR_PACIENTE.place(x=1000, y=220, width=150, height=50)

################################### Janela para confirmar procedimento################

LISTA_PROCEDIMENTOS = ["Restauração de Resina Composta", "Restauração de Amalgama Dental", "Restauração de Cimento de Ionômero de Vidro", "Limpeza Simples", "Limpeza Completa", "Exodontia", "Raspagem", "Endodontia", "Gengivoplastia","Manutenção de Aparelho Ortodontico", "Protese Fixa", "Protese Total", "Protese Parcial Removivel"]
NUMERO_DOS_DENTES = ["11","12", "13", "14", "15", "16", "17", "18", "21", "22", "23", "24", "25", "26", "27", "28", "31", "32", "33", "34", "35", "36", "37", "38", "41", "42", "43", "44", "45", "46", "47", "48", "51", "52", "53", "54", "55", "61", "62", "63", "64", "65", "71", "72", "73", "74", "75", "81", "82", "83", "84", "85", "Supranumerário"]
FACES_DOS_DENTES = ["Vestibular", "Lingua/Palatina", "Mesial", "Disatal", "Oclusal/Incisal"]


################################### Aba de historico do paciente######################
def pesquisarHistorico():
    try:
        TELA_HISTORICO.delete(*TELA_HISTORICO.get_children())
        VALOR_ENTRY = ENT_PACIENTES.get().upper()
        vquery = "SELECT DATA, PROCEDIMENTO, DENTE, FACE, VALOR FROM procedimentos WHERE NOME='"+VALOR_ENTRY+"'" 
        linhas = conexao.dql(vquery)
        for i in linhas:
            TELA_HISTORICO.insert("", "end", values=i)
    except:
        print(ValueError)

VQUERY_LISTA = "SELECT NOME FROM procedimentos"
LINHAS_LISTA = conexao.dql(VQUERY_LISTA)

HISTORICO = Frame(ABAS)
ABAS.add(HISTORICO, text="Histórico")

L_PACIENTES = Label(HISTORICO, text="Paciente")
L_PACIENTES.place(x=10, y=10)
ENT_PACIENTES = ttk.Combobox(HISTORICO, values=LINHAS_LISTA)
ENT_PACIENTES.place(x=10, y=40, width=400, height=25)
BOTAO_PESQUISAR_HISTORICO = Button(HISTORICO, text="Pesquisar", command=pesquisarHistorico)
BOTAO_PESQUISAR_HISTORICO.place(x=440, y=40, width=100)
TELA_HISTORICO = ttk.Treeview(HISTORICO, columns=("DATA", "PROCEDIMENTO", "DENTE", "FACE", "VALOR"), show="headings", padding=2)
TELA_HISTORICO.column("DATA", minwidth=0, width=30)
TELA_HISTORICO.column("PROCEDIMENTO", minwidth=0, width=300)
TELA_HISTORICO.column("DENTE", minwidth=0, width=30)
TELA_HISTORICO.column("FACE", minwidth=0, width=30)
TELA_HISTORICO.column("VALOR", minwidth=0, width=30)
TELA_HISTORICO.heading("DATA", text="DATA")
TELA_HISTORICO.heading("PROCEDIMENTO", text="PROCEDIMENTO")
TELA_HISTORICO.heading("DENTE", text="DENTE")
TELA_HISTORICO.heading("FACE", text="FACE")
TELA_HISTORICO.heading("VALOR", text="VALOR")
TELA_HISTORICO.place(x=10, y=90, width=1180, height=450)

############################################################# Relatório ###########################################################

def pesquisarRelatorio():
    if LISTA_RELATORIO.get() == "Diário":
        TELA_RELATORIO.delete(*TELA_RELATORIO.get_children())
        vquery = "SELECT NOME, DATA, VALOR FROM procedimentos WHERE DATA='"+COMB_DIA_RELATORIO.get()+"/"+COMB_MES_RELATORIO.get()+"/"+COMB_ANO_RELATORIO.get()+"'"
        linhas = conexao.dql(vquery)
        for i in linhas:
            TELA_RELATORIO.insert("", "end", values=i)
        ENT_VALOR_TOTAL.delete(0,END)
        vquery_1 = "SELECT SUM(VALOR) FROM procedimentos WHERE DATA='"+COMB_DIA_RELATORIO.get()+"/"+COMB_MES_RELATORIO.get()+"/"+COMB_ANO_RELATORIO.get()+"'"
        linhas_1 = conexao.dql(vquery_1)
        ENT_VALOR_TOTAL.insert(END, linhas_1)
        ENT_NUM_PACIENTES.delete(0, END)
        vquery_2 = "SELECT COUNT(NOME) FROM procedimentos WHERE DATA='"+COMB_DIA_RELATORIO.get()+"/"+COMB_MES_RELATORIO.get()+"/"+COMB_ANO_RELATORIO.get()+"'"
        linhas_2 = conexao.dql(vquery_2)
        ENT_NUM_PACIENTES.insert(END, linhas_2)
    elif LISTA_RELATORIO.get() == "Mensal":
        TELA_RELATORIO.delete(*TELA_RELATORIO.get_children())
        vquery = "SELECT NOME, DATA, VALOR FROM procedimentos WHERE DATA LIKE '%"+COMB_MES_RELATORIO.get()+"%'"
        linhas = conexao.dql(vquery)
        for i in linhas:
            TELA_RELATORIO.insert("", "end", values=i)
        ENT_VALOR_TOTAL.delete(0,END)
        vquery_1 = "SELECT SUM(VALOR) FROM procedimentos WHERE DATA LIKE '%"+COMB_MES_RELATORIO.get()+"%'"
        linhas_1 = conexao.dql(vquery_1)
        ENT_VALOR_TOTAL.insert(END, linhas_1)
        ENT_NUM_PACIENTES.delete(0, END)
        vquery_2 = "SELECT COUNT(NOME) FROM procedimentos WHERE DATA LIKE '%"+COMB_MES_RELATORIO.get()+"%'"
        linhas_2 = conexao.dql(vquery_2)
        ENT_NUM_PACIENTES.insert(END, linhas_2)
    elif LISTA_RELATORIO.get() == "Anual":
        TELA_RELATORIO.delete(*TELA_RELATORIO.get_children())
        vquery = "SELECT NOME, DATA, VALOR FROM procedimentos WHERE DATA LIKE '%"+COMB_ANO_RELATORIO.get()+"'"
        linhas = conexao.dql(vquery)
        for i in linhas:
            TELA_RELATORIO.insert("", "end", values=i)
        ENT_VALOR_TOTAL.delete(0,END)
        vquery_1 = "SELECT SUM(VALOR) FROM procedimentos WHERE DATA LIKE '%"+COMB_ANO_RELATORIO.get()+"'"
        linhas_1 = conexao.dql(vquery_1)
        ENT_VALOR_TOTAL.insert(END, linhas_1)
        ENT_NUM_PACIENTES.delete(0, END)
        vquery_2 = "SELECT COUNT(NOME) FROM procedimentos WHERE DATA LIKE '%"+COMB_ANO_RELATORIO.get()+"'"
        linhas_2 = conexao.dql(vquery_2)
        ENT_NUM_PACIENTES.insert(END, linhas_2)

RELATORIO = Frame(ABAS)
ABAS.add(RELATORIO, text="Relatório")

COMB_LISTA_RELATORIO = "Diário", "Mensal", "Anual"


LF_LISTA_RELATORIO = LabelFrame(RELATORIO, text="Tipos de Relatório")
LF_LISTA_RELATORIO.place(x=10, y=10, width=1180, height=100)
LF_DATA = LabelFrame(LF_LISTA_RELATORIO)
LF_DATA.place(x=500, y=10, width=650, height=60)
L_DATA_RELATORIO = Label(LF_DATA, text="Selecione a data a ser consultada:")
L_DATA_RELATORIO.place(x=10, y=20)
L_DIA_RELATORIO = Label(LF_DATA, text="Dia")
L_MES_RELATORIO = Label(LF_DATA, text="Mês")
L_ANO_RELATORIO = Label(LF_DATA, text="Ano")
L_DIA_RELATORIO.place(x=250, y=5)
L_MES_RELATORIO.place(x=310, y=5)
L_ANO_RELATORIO.place(x=380, y=5)
COMB_DIA_RELATORIO = ttk.Combobox(LF_DATA, values=LISTA_DIAS)
COMB_MES_RELATORIO = ttk.Combobox(LF_DATA, values=LISTA_MES)
COMB_ANO_RELATORIO = ttk.Combobox(LF_DATA, values=LISTA_ANO)
COMB_DIA_RELATORIO.place(x=240, y=25, width=40, height=25)
COMB_MES_RELATORIO.place(x=285, y=25, width=80, height=25)
COMB_ANO_RELATORIO.place(x=370, y=25, width=50, height=25)
BTN_PESQUISAR_RELATORIO = Button(LF_DATA, text="Pesquisar", command=pesquisarRelatorio)
BTN_PESQUISAR_RELATORIO.place(x=450, y=25, width=150)
L_LISTA_RELATORIO = Label(LF_LISTA_RELATORIO, text="Selecione a opção de relatório desejada")
L_LISTA_RELATORIO.place(x=10, y=10)
LISTA_RELATORIO = ttk.Combobox(LF_LISTA_RELATORIO, values=COMB_LISTA_RELATORIO)
LISTA_RELATORIO.place(x=10, y=40, width=300, height=25)
TELA_RELATORIO = ttk.Treeview(RELATORIO, columns=("NOME", "DATA", "VALOR"), show="headings", padding=2)
TELA_RELATORIO.column("NOME", minwidth=0, width=300)
TELA_RELATORIO.column("DATA", minwidth=0, width=30)
TELA_RELATORIO.column("VALOR", minwidth=0, width=30)
TELA_RELATORIO.heading("NOME", text="NOME")
TELA_RELATORIO.heading("DATA", text="DATA")
TELA_RELATORIO.heading("VALOR", text="VALOR")
TELA_RELATORIO.place(x=10, y=120, width=1180, height=300)
LF_RESUMO_RELATORIO = LabelFrame(RELATORIO, text="Resumo")
LF_RESUMO_RELATORIO.place(x=10, y=450, width=1180, height=100)
L_VALOR_TOTAL = Label(LF_RESUMO_RELATORIO, text="Valor Total:")
L_VALOR_TOTAL.place(x=10,y=10)
ENT_VALOR_TOTAL = Entry(LF_RESUMO_RELATORIO)
ENT_VALOR_TOTAL.place(x=100, y=10, width=300)
L_NUM_PACIENTES = Label(LF_RESUMO_RELATORIO, text="Número de Pacientes Atendidos:")
L_NUM_PACIENTES.place(x=10, y=40)
ENT_NUM_PACIENTES = Entry(LF_RESUMO_RELATORIO)
ENT_NUM_PACIENTES.place(x=200, y=40, width=200)

mainloop()