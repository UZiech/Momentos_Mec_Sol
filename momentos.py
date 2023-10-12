from tkinter import *
from pkg_resources import resource_filename

##############################
##Desenha as cargas pontuais##
##############################
def desenha_qp(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_dist):

    x0=37
    xf=412
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    if not canvas.gettags("qp"):
        #esses ifs são para verificar se as cargas pontuais são maiores que zero. Se forem maiores que zero, aí desenham o vetor
        if valor_q1>0:
            canvas.create_polygon(x0+valor_x1*a-10,248,x0+valor_x1*a, 278,x0+valor_x1*a+10,248, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x1*a,278, x0+valor_x1*a, 178, fill="blue", width=2,tags="qp")

        if valor_q2>0:
            canvas.create_polygon(x0+valor_x2*a-10,248,x0+valor_x2*a, 278,x0+valor_x2*a+10,248, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x2*a,278, x0+valor_x2*a, 178, fill="blue", width=2,tags="qp")

        if valor_q3>0:
            canvas.create_polygon(x0+valor_x3*a-10,248,x0+valor_x3*a, 278,x0+valor_x3*a+10,248, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x3*a,278, x0+valor_x3*a, 178, fill="blue", width=2,tags="qp")

        if valor_q4>0:
            canvas.create_polygon(x0+valor_x4*a-10,248,x0+valor_x4*a, 278,x0+valor_x4*a+10,248, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x4*a,278, x0+valor_x4*a, 178, fill="blue", width=2,tags="qp")

        if valor_q5>0:
            canvas.create_polygon(x0+valor_x5*a-10,248,x0+valor_x5*a, 278,x0+valor_x5*a+10,248, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x5*a,278, x0+valor_x5*a, 178, fill="blue", width=2,tags="qp")
    else:
        canvas.delete("qp")


##################################
##Desenha as cargas distribuidas##
##################################
def desenha_ql(valor_ql,valor_qlxi,valor_qlxf,valor_dist):
    x0=37
    xf=412
    espacamento_vetores=50 #espaçamento entre vetores em pixel
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga
    
    if not canvas.gettags("ql"):
        if valor_ql > 0:
            qtd_vetores = int((valor_qlxf*a-valor_qlxi*a)/espacamento_vetores)
            xi=valor_qlxi

        #Se a distancia final for muito proximo da inicial da carga distribuida, recaira em divisão por zero. Esse if é para evitar divisao por zero
            if qtd_vetores <= 1:
                qtd_vetores=1
        
            incremento=float((valor_qlxf-valor_qlxi)/(qtd_vetores))

        #cria os vetores de força devido a carga distribuida
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,268,x0+xi*a, 278,x0+xi*a+5,268, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,278, x0+xi*a, 228, fill="green", width=2,tag="ql")
                xi=xi+incremento
                
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+valor_qlxi*a,228, x0+valor_qlxf*a, 228, fill="green", width=2,tag="ql")
    else:
        canvas.delete("ql")


###########################################################################
##Função que mostra o grafico e e chama as funcoes que desenham as cargas##
###########################################################################
def desenha(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_ql,valor_qlxi,valor_qlxf,valor_dist):
    #Desenha os pontos de apoio - primeiro o da esquereda, depois o da direita e depois a viga
    #Desenho do apoio da esquerda - engastado
    canvas.create_polygon(25, 300, 50, 300, 37, 278, 25, 300, outline="black", width = 2, fill="white")
    canvas.create_line(25,305,30,300)
    canvas.create_line(30,305,35,300)
    canvas.create_line(35,305,40,300)
    canvas.create_line(40,305,45,300)
    canvas.create_line(45,305,50,300)

    #Desenho do apoio da direita - movel
    canvas.create_polygon(400, 300, 425, 300, 412, 278, 400, 300, outline="black", width = 2, fill="white")
    canvas.create_oval(400, 305, 405, 300, fill="white")
    canvas.create_oval(405, 305, 410, 300, fill="white")
    canvas.create_oval(410, 305, 415, 300, fill="white")
    canvas.create_oval(415, 305, 420, 300, fill="white")
    canvas.create_oval(420, 305, 425, 300, fill="white")
    canvas.create_line(385,310,390,305)
    canvas.create_line(390,305,435,305)
    canvas.create_line(395,310,400,305)
    canvas.create_line(405,310,410,305)
    canvas.create_line(415,310,420,305)
    canvas.create_line(425,310,430,305)

    #Desenho da viga
    canvas.create_line(37, 278, 412, 278, width = 4, fill="black")    
    
    #Dispões o gráfco no grid
    canvas.grid(column=6, row=0, padx=10, pady=10, rowspan=9,columnspan=2)
    
    #Inicializa e mostra os botoes que irao chamar as funções para exibir as cargas pontuais ou distribuida
    botao_qp = Button(main, text="Cargas Pontuais", command=lambda: desenha_qp(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_dist))
    botao_ql = Button(main, text="Cargas Distribuidas", command=lambda: desenha_ql(valor_ql,valor_qlxi,valor_qlxf,valor_dist))
    botao_qp.grid(column=6, row=10, padx=10, pady=10)
    botao_ql.grid(column=7, row=10, padx=10, pady=10)

    return botao_qp, botao_ql

####################################################################
##Função que habilita novas entradas, para permitir novos calculos##
####################################################################

def habilita_entradas(botao_novos_valores, botao_qp, botao_ql):
    q1.config(state="normal")
    q2.config(state="normal")
    q3.config(state="normal")
    q4.config(state="normal")
    q5.config(state="normal")

    x1.config(state="normal")
    x2.config(state="normal")
    x3.config(state="normal")
    x4.config(state="normal")
    x5.config(state="normal")
    
    ql.config(state="normal")
    qlxi.config(state="normal")
    qlxf.config(state="normal")
    dist.config(state="normal")

    #retira o botao que habilita as entrada e insere o botao calcular no lugar
    botao_novos_valores.grid_forget()
    botao_calcular.grid(column=4, row=10, padx=10, pady=10)
    canvas.delete("all")
    canvas.grid_forget()
    botao_qp.grid_forget()
    botao_ql.grid_forget()

######################################################################
##Função que desabilita novas entradas, para não confundir o usuario##
######################################################################

def desabilita_entradas(botao_qp, botao_ql):
    q1.config(state="disabled")
    q2.config(state="disabled")
    q3.config(state="disabled")
    q4.config(state="disabled")
    q5.config(state="disabled")

    x1.config(state="disabled")
    x2.config(state="disabled")
    x3.config(state="disabled")
    x4.config(state="disabled")
    x5.config(state="disabled")
    
    ql.config(state="disabled")
    qlxi.config(state="disabled")
    qlxf.config(state="disabled")
    dist.config(state="disabled")

    botao_calcular.grid_forget()
    #Inicialia o botao que permite inserir novos valores
    botao_novos_valores = Button(main, text="Novos Valores", command=lambda: habilita_entradas(botao_novos_valores, botao_qp, botao_ql))
    botao_novos_valores.grid(column=4, row=10, padx=10, pady=10)


###############################################################  
#Funcao que checa a validade do valor fornecido pelo usuario###
###############################################################
def valida_entrada():
    #testa se os valores fornecidos pelo usuarios estao corretos
    try:
        float(q1.get())
        float(q2.get())
        float(q3.get())
        float(q4.get())
        float(q5.get())

        float(x1.get())
        float(x2.get())
        float(x3.get())
        float(x4.get())
        float(x5.get())

        float(ql.get())
        float(qlxi.get())
        float(qlxf.get())
        float(dist.get())
 
        info3["text"] = ""
    except:
        info3["text"] = "Apenas números, sinal negaitivo ou separador decimal."
        return False  

    #atribui o valor fornecido pelo usuarios para as variaveis
    valor_q1 = float(q1.get())
    valor_q2 = float(q2.get())
    valor_q3 = float(q3.get())
    valor_q4 = float(q4.get())
    valor_q5 = float(q5.get())

    valor_x1 = float(x1.get())
    valor_x2 = float(x2.get())
    valor_x3 = float(x3.get())
    valor_x4 = float(x4.get())
    valor_x5 = float(x5.get())

    valor_ql = float(ql.get())
    valor_qlxi = float(qlxi.get())
    valor_qlxf = float(qlxf.get())
    valor_dist = float(dist.get())

    if valor_dist < 0:
        info3["text"] = "Deve ser fornecido valor positivo para a distância"
        return False

    elif valor_x1 < 0 or valor_x1 > valor_dist:
        info3["text"] = "A carga 1 estás fora da viga. Corrigir."
        return False
    
    elif valor_x2 < 0 or valor_x2 > valor_dist:
        info3["text"] = "A carga 2 está fora da viga. Corrigir."
        return False

    elif valor_x3 < 0 or valor_x3 > valor_dist:
        info3["text"] = "A carga 3 está fora da viga. Corrigir."
        return False
    
    elif valor_x4 < 0 or valor_x4 > valor_dist:
        info3["text"] = "A carga 4 está fora da viga. Corrigir."
        return False
    
    elif valor_x5 < 0 or valor_x5 > valor_dist:
        info3["text"] = "A carga 5 está fora da viga. Corrigir."
        return False
    
    elif valor_qlxi < 0 or valor_qlxi > valor_dist:
        info3["text"] = "Parte da carga distribuída está fora da viga. Corrigir."
        return False

    elif valor_qlxf < 0 or valor_qlxf > valor_dist:
        info3["text"] = "Parte da carga distribuída está fora da viga. Corrigir."
        return False
    
    elif valor_qlxf < valor_qlxi:
        info3["text"] = "Corrigir valores de início e fim da carga distribuida."
        return False    

    else:
        #Se não ocorreram erros, faz o desenho da viga, apoio e forças
        botao_qp, botao_ql = desenha(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_ql,valor_qlxi,valor_qlxf,valor_dist)
        desabilita_entradas(botao_qp, botao_ql)

###################################
##Função Main - Interface Gráfica##
###################################
main = Tk()
main.title("Mecanica dos solidos 1 - Diagrama de momentos")
#main.geometry("480x500")
resource1 = resource_filename(__name__, 'favicon.ico')
main.iconbitmap(resource1)

#Inicia as variaveis para os campos de entrada com o texto padrao
qp1 = StringVar()
qp2 = StringVar()
qp3 = StringVar()
qp4 = StringVar()
qp5 = StringVar()
qp1.set("0.00")
qp2.set("0.00")
qp3.set("0.00")
qp4.set("0.00")
qp5.set("0.00")

xp1 = StringVar()
xp2 = StringVar()
xp3 = StringVar()
xp4 = StringVar()
xp5 = StringVar()
xp1.set("0.00")
xp2.set("0.00")
xp3.set("0.00")
xp4.set("0.00")
xp5.set("0.00")

qlp = StringVar()
qlxip = StringVar()
qlxfp = StringVar()
distp = StringVar()
qlp.set("0.00")
qlxip.set("0.00")
qlxfp.set("0.00")
distp.set("2.00")

q1 = Entry(main, width=10, textvariable=qp1)
q2 = Entry(main, width=10, textvariable=qp2)
q3 = Entry(main, width=10, textvariable=qp3)
q4 = Entry(main, width=10, textvariable=qp4)
q5 = Entry(main, width=10, textvariable=qp5)

x1 = Entry(main, width=10, textvariable=xp1)
x2 = Entry(main, width=10, textvariable=xp2)
x3 = Entry(main, width=10, textvariable=xp3)
x4 = Entry(main, width=10, textvariable=xp4)
x5 = Entry(main, width=10, textvariable=xp5)

ql = Entry(main, width=10, textvariable=qlp)
qlxi = Entry(main, width=10, textvariable=qlxip)
qlxf = Entry(main, width=10, textvariable=qlxfp)
dist = Entry(main, width=10, textvariable=distp)

#Inicia as variaveis de texto
info1=Label(main, text="Forneça apenas valores numéricos com separador decimal sendo o ponto.")
info2 = Label(main, text="Distância entre os pontos de apoio em metros.")
info3 = Label(main, text="", font="Arial", fg="red")
texto_1=Label(main, text="Carga 1:")
texto_2=Label(main, text="Carga 2:")
texto_3=Label(main, text="Carga 3:")
texto_4=Label(main, text="Carga 4:")
texto_5=Label(main, text="Carga 5:")
texto_qpkn=Label(main, text="Q (KN)")
texto_qlkn=Label(main, text="Q (KN/m):")
texto_x=Label(main, text="X (m)")
texto_inicio=Label(main, text="Inicio (m):")
texto_fim=Label(main, text="Fim (m):")
texto_dist=Label(main, text="Distancia:")

texto_qp=Label(main, text="Cargas Pontuais")
texto_ql=Label(main, text="Carga Distribuida")


###################################
##Organizacao dos widget por grid##
###################################
#informação de preenchimento ao usuario
info1.grid(column=0, row=0, padx=10, pady=10, columnspan=6)

#Textos informativos aos usuarios
texto_1.grid(column=0, row=4, padx=10)
texto_2.grid(column=0, row=5, padx=10, pady=10)
texto_3.grid(column=0, row=6, padx=10, pady=10)
texto_4.grid(column=0, row=7, padx=10, pady=10)
texto_5.grid(column=0, row=8, padx=10, pady=10)

texto_qpkn.grid(column=1, row=3, padx=10, pady=10)
texto_qlkn.grid(column=4, row=4, padx=10, pady=10)
texto_x.grid(column=2, row=3, padx=10, pady=10)
texto_inicio.grid(column=4, row=5, padx=10, pady=10)
texto_fim.grid(column=4, row=6, padx=10, pady=10)
texto_dist.grid(column=0, row=10, padx=10, pady=10)

texto_qp.grid(column=0, row=2, columnspan=4)
texto_ql.grid(column=4, row=2, columnspan=2)

#Box de entrada de dados
q1.grid(column=1, row=4, padx=10)
q2.grid(column=1, row=5, padx=10, pady=10)
q3.grid(column=1, row=6, padx=10, pady=10)
q4.grid(column=1, row=7, padx=10, pady=10)
q5.grid(column=1, row=8, padx=10, pady=10)

x1.grid(column=2, row=4, padx=10)
x2.grid(column=2, row=5, padx=10, pady=10)
x3.grid(column=2, row=6, padx=10, pady=10)
x4.grid(column=2, row=7, padx=10, pady=10)
x5.grid(column=2, row=8, padx=10, pady=10)

ql.grid(column=5, row=4, padx=10)
qlxi.grid(column=5, row=5, padx=10, pady=10)
qlxf.grid(column=5, row=6, padx=10, pady=10)
dist.grid(column=1, row=10, padx=10, pady=10)

#Tela de desenhos
canvas = Canvas(main, width=450, height=350, bg="white")

#Inicializacao e posicionamento do botao calcular
#Após o usuario clicar no botao, chama a função que realiza as checagens e essa, chama a funcao que realiza os calculos
botao_calcular = Button(main, text="Calcular", command=valida_entrada)
botao_calcular.grid(column=4, row=10, padx=10, pady=10)

#Mostra os resultados da conferencia dos dados de entrada
info2.grid(column=0, row=9, padx=10, pady=10, columnspan=6)
info3.grid(column=0, row=11, padx=10, pady=10, columnspan=6)

#Inicializacao e posicionamento do botao sair
botao_sair = Button(master=main, text="Sair", command=main.destroy)
botao_sair.grid(column=5, row=10)

main.mainloop()