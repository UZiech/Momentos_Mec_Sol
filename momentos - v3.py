from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pkg_resources import resource_filename


##############################
##Desenha as cargas pontuais##
##############################
def desenha_qp(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_dist):

    x0=37
    xf=412
    yb=hc-hc/3
    yv=yb-22
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    #se já tinha algo desenhado, não faz nada e entra na condição else, que retira os vetores do desenho
    if not canvas.gettags("qp"):
        #esses ifs são para verificar se as cargas pontuais são maiores que zero para desenhar a seta no sentido correto
        if valor_q1<0:
            canvas.create_polygon(x0+valor_x1*a-10,yv-20,x0+valor_x1*a, yv,x0+valor_x1*a+10,yv-20, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x1*a,yv-20, x0+valor_x1*a, yv-82, fill="blue", width=2,tags="qp")
        elif valor_q1>0:
            canvas.create_polygon(x0+valor_x1*a-10,yb,x0+valor_x1*a, yv,x0+valor_x1*a+10,yb, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x1*a,yb, x0+valor_x1*a, yv+82, fill="blue", width=2,tags="qp")

        if valor_q2<0:
            canvas.create_polygon(x0+valor_x2*a-10,yv-20,x0+valor_x2*a, yv,x0+valor_x2*a+10,yv-20, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x2*a,yv-20, x0+valor_x2*a, yv-82, fill="blue", width=2,tags="qp")
        elif valor_q2>0:
            canvas.create_polygon(x0+valor_x2*a-10,yb,x0+valor_x2*a, yv,x0+valor_x2*a+10,yb, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x2*a,yb, x0+valor_x2*a, yv+82, fill="blue", width=2,tags="qp")

        if valor_q3<0:
            canvas.create_polygon(x0+valor_x3*a-10,yv-20,x0+valor_x3*a, yv,x0+valor_x3*a+10,yv-20, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x3*a,yv-20, x0+valor_x3*a, yv-82, fill="blue", width=2,tags="qp")
        elif valor_q3>0:
            canvas.create_polygon(x0+valor_x3*a-10,yb,x0+valor_x3*a, yv,x0+valor_x3*a+10,yb, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x3*a,yb, x0+valor_x3*a, yv+82, fill="blue", width=2,tags="qp")

        if valor_q4<0:
            canvas.create_polygon(x0+valor_x4*a-10,yv-20,x0+valor_x4*a, yv,x0+valor_x4*a+10,yv-20, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x4*a,yv-20, x0+valor_x4*a, yv-82, fill="blue", width=2,tags="qp")
        elif valor_q4>0:
            canvas.create_polygon(x0+valor_x4*a-10,yb,x0+valor_x4*a, yv,x0+valor_x4*a+10,yb, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x4*a,yb, x0+valor_x4*a, yv+82, fill="blue", width=2,tags="qp")

        if valor_q5<0:
            canvas.create_polygon(x0+valor_x5*a-10,yv-20,x0+valor_x5*a, yv,x0+valor_x5*a+10,yv-20, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x5*a,yv-20, x0+valor_x5*a, yv-82, fill="blue", width=2,tags="qp")
        elif valor_q5>0:
            canvas.create_polygon(x0+valor_x5*a-10,yb,x0+valor_x5*a, yv,x0+valor_x5*a+10,yb, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+valor_x5*a,yb, x0+valor_x5*a, yv+82, fill="blue", width=2,tags="qp")
    else:
        canvas.delete("qp")


##################################
##Desenha as cargas distribuidas##
##################################
def desenha_ql(valor_ql,valor_qlxi,valor_qlxf,valor_dist):
    x0=37
    xf=412
    yb=hc-hc/3
    yv=yb-22

    espacamento_vetores=50 #espaçamento entre vetores em pixel
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga
    qtd_vetores = int((valor_qlxf*a-valor_qlxi*a)/espacamento_vetores)
    xi=valor_qlxi
    
    #Se a distancia final for muito proximo da inicial da carga distribuida, recaira em divisão por zero. Esse if é para evitar divisao por zero
    if qtd_vetores <= 1:
        qtd_vetores=1

    incremento=float((valor_qlxf-valor_qlxi)/(qtd_vetores)) 

        
    #se já tinha algo desenhado, não faz nada e entra na condição else, que retira os vetores do desenho    
    if not canvas.gettags("ql"):

        #cria os vetores de força devido a carga distribuida
        if valor_ql < 0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv-10,x0+xi*a, yv,x0+xi*a+5,yv-10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv-82, fill="green", width=2,tag="ql")
                xi=xi+incremento
                
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+valor_qlxi*a,yv-82, x0+valor_qlxf*a, yv-82, fill="green", width=2,tag="ql")
        elif valor_ql >0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv+10,x0+xi*a, yv,x0+xi*a+5,yv+10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv+82, fill="green", width=2,tag="ql")
                xi=xi+incremento
                
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+valor_qlxi*a,yv+82, x0+valor_qlxf*a, yv+82, fill="green", width=2,tag="ql")

    else:
        canvas.delete("ql")



###########################################################################
##Função que mostra o grafico e e chama as funcoes que desenham as cargas##
###########################################################################
def desenha():
    #coordenadas de posicionamento do desenho
    yb=hc-hc/3
    valor_dist=float(coord_ex_entry.get())-float(coord_dx_entry.get())

    #Desenha os pontos de apoio - primeiro o da esquereda, depois o da direita e depois a viga
    #Desenho do apoio da esquerda - engastado
    canvas.create_polygon(25, yb, 50, yb, 37, yb-22, 25, yb, outline="black", width = 2, fill="white")
    canvas.create_line(25,yb+5,30,yb)
    canvas.create_line(30,yb+5,35,yb)
    canvas.create_line(35,yb+5,40,yb)
    canvas.create_line(40,yb+5,45,yb)
    canvas.create_line(45,yb+5,50,yb)

    #Desenho do apoio da direita - movel
    canvas.create_polygon(400, yb, 425, yb, 412, yb-22, 400, yb, outline="black", width = 2, fill="white")
    canvas.create_oval(400, yb+5, 405, yb, fill="white")
    canvas.create_oval(405, yb+5, 410, yb, fill="white")
    canvas.create_oval(410, yb+5, 415, yb, fill="white")
    canvas.create_oval(415, yb+5, 420, yb, fill="white")
    canvas.create_oval(420, yb+5, 425, yb, fill="white")
    canvas.create_line(385,yb+10,390,yb+5)
    canvas.create_line(390,yb+5,435,yb+5)
    canvas.create_line(395,yb+10,400,yb+5)
    canvas.create_line(405,yb+10,410,yb+5)
    canvas.create_line(415,yb+10,420,yb+5)
    canvas.create_line(425,yb+10,430,yb+5)

    #Desenho da viga
    canvas.create_line(37, yb-22, 412, yb-22, width = 4, fill="black")    
    
    #Dispões o gráfco no grid
    canvas.grid(column=6, row=0, padx=10, pady=10, rowspan=10,columnspan=3)
    
    #Inicializa e mostra os botoes que irao chamar as funções para exibir as cargas pontuais ou distribuida
    botao_qp = Button(frame_grafico, text="Cargas Pontuais", command=lambda: desenha_qp(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_dist))
    botao_ql = Button(frame_grafico, text="Cargas Distribuidas", command=lambda: desenha_ql(valor_ql,valor_qlxi,valor_qlxf,valor_dist))
    botao_reacao = Button(frame_grafico, text="Reação", command=lambda: forca_reacao(valor_x1,valor_x2,valor_x3,valor_x4,valor_x5,valor_q1,valor_q2,valor_q3,valor_q4,valor_q5,valor_ql,valor_qlxi,valor_qlxf,valor_dist))
    botao_qp.grid(column=6, row=10, padx=10, pady=10)
    botao_ql.grid(column=7, row=10, padx=10, pady=10)
    botao_reacao.grid(column=8, row=10, padx=10, pady=10)

    return botao_qp, botao_ql, botao_reacao

#########################################################  
#Funcao que lista as cargas já fornecidas pelo usuario###
#########################################################
def listar_cargas():
    relacao_qp["text"]="Cargas Pontuais\n"
    for i in range(0,len(qp),3):
        j=i+1
        k=i+2
        relacao_qp["text"] = relacao_qp["text"] + "F" + str(int(i/3)+1) + "= " + str(qp[i]) + "i + " + str(qp[j]) + "j Ponto de atuação X= " + str(qp[k]) + "m.\n"

    relacao_qd["text"] = "Cargas distribuidas\n"
    for i in range(0,len(qd),4):
        j=i+1
        k=i+2
        z=i+3
        relacao_qd["text"] = relacao_qd["text"]+"F"+str(int(i/4)+1)+"= "+str(qd[i])+"i + "+str(qd[j])+"j Inicio de aplicação Xi= "+str(qd[k])+"m Fim de aplicação Xf= "+ str(qd[z]) +"m.\n"

#########################################################  
#Funcao que lista as cargas já fornecidas pelo usuario###
#########################################################
def remover_cargas():
    tipo=combobox.get()
    indice=int(carga_entry.get())
    indice=(indice-1)

    match tipo:
        case "Carga pontual":
            qp.pop(3*indice)
            qp.pop(3*indice)
            qp.pop(3*indice)
            
        case"Carga Distribuida":
            qd.pop(4*indice)
            qd.pop(4*indice)
            qd.pop(4*indice)
            qd.pop(4*indice)
    listar_cargas()   


###############################################################  
#Funcao que checa a validade do valor fornecido pelo usuario###
###############################################################
def valida_entrada(tipo, lista):
    match tipo:
        case 'qp':
            try:
                float(qpfx_entry.get())
                float(qpfy_entry.get())
                float(qpxi_entry.get())
            except:
                messagebox.showerror(title="Info", message="Somente números, positivos ou negativos.\nSeparador decimal deve ser o ponto!")
                return False


            lista.append(float(qpfx_entry.get()))
            lista.append(float(qpfy_entry.get()))
            lista.append(float(qpxi_entry.get()))
            listar_cargas()

        case 'qd':
            try:
                float(qdfx_entry.get())
                float(qdfy_entry.get())
                float(qdxi_entry.get())
                float(qdxf_entry.get())
            except:
                messagebox.showerror(title="Info", message="Somente números, positivos ou negativos.\nSeparador decimal deve ser o ponto!")
                return False

            lista.append(float(qdfx_entry.get()))
            lista.append(float(qdfy_entry.get()))
            lista.append(float(qdxi_entry.get()))
            lista.append(float(qdxf_entry.get()))
            listar_cargas()

        case 'remover':
            try:
                int(carga_entry.get())
            except:
                messagebox.showerror(title="Info", message="Somente números positivos inteiros.")
                return False
            if combobox.get() == "Carga pontual":
                if int(carga_entry.get()) > len(qp)/3:
                    messagebox.showerror(title="Info", message="Não existe a referida carga aplicada.\nDica: verifique o índice da carga na listagem de cargas já aplicadas!")
                    return False
                elif int(carga_entry.get()) < 1:
                    messagebox.showerror(title="Info", message="Não existe a referida carga aplicada.\nDica: verifique o índice da carga na listagem de cargas já aplicadas!")
                    return False
            elif combobox.get() == "Carga Distribuida":
                if int(carga_entry.get()) > len(qd)/4:
                    messagebox.showerror(title="Info", message="Não existe a referida carga aplicada.\nDica: verifique o índice da carga na listagem de cargas já aplicadas!")
                    return False
                elif int(carga_entry.get()) < 1:
                    messagebox.showerror(title="Info", message="Não existe a referida carga aplicada.\nDica: verifique o índice da carga na listagem de cargas já aplicadas!")
                    return False

            remover_cargas()

        case 'apoio':
            valores_xqp=[]
            valores_xiqd=[]
            valores_xfqd=[]

            try:
                float(coord_ex_entry.get())
                float(coord_dx_entry.get())
            except:
                messagebox.showerror(title="Info", message="Somente números, positivos ou negativos.\nSeparador decimal deve ser o ponto!")
                return False
            
            #verifica se a coordenada esquerda é maior que a direita.
            if float(coord_ex_entry.get()) > float(coord_dx_entry.get()) :
                messagebox.showerror(title="Info", message="Corrija o posicionamento dos pontos de apoio. Estão trocados")
                return False
            
            if (len(qp) == 0) and (len(qd) == 0):
                messagebox.showerror(title="Info", message="Necessário lançar ao menos 1 carga, seja pontual ou continua.")
                return False


            #Verifica se existem cargas pontuais e depois verifica se existem cargas fora das dimensoes da viga
            if not (len(qp) == 0):
                
                #Coleta as coordenadas x de todas as forças pontuais, para depois descobir qual a menor e saber se ela é menor que a apoio esquerdo da viga
                for i in range(0,len(qp),3):
                    valores_xqp.append(qp[i+2])

                if min(valores_xqp) < float(coord_ex_entry.get()):
                    messagebox.showerror(title="Info", message="A Viaga não abrange todas as cargas aplicadas.\nAumente o tamanho da viga ou remova as cargas que estão fora.")
                    return False

                elif max(valores_xqp) > float(coord_dx_entry.get()):
                    messagebox.showerror(title="Info", message="A Viaga não abrange todas as cargas aplicadas.\nAumente o tamanho da viga ou remova as cargas que estão fora.")
                    return False
                
            #Verifica se existem cargas distribuidas e depois verifica se existem cargas fora das dimensoes da viga
            if not (len(qd) == 0):

                #Coleta as coordenadas xinicial e xfinial de todas as forças distribuidas, para depois descobir qual o menor xi e o maior xf para comprar com as dimensoes da viga
                for i in range(0,len(qd),4):
                    valores_xiqd.append(qd[i+2])
                    valores_xfqd.append(qd[i+3])
                    
                if min(valores_xiqd) < float(coord_ex_entry.get()):
                    messagebox.showerror(title="Info", message="A Viaga não abrange todas as cargas aplicadas.\nAumente o tamanho da viga ou remova as cargas que estão fora.")
                    return False

                elif max(valores_xfqd) > float(coord_dx_entry.get()):
                    messagebox.showerror(title="Info", message="A Viaga não abrange todas as cargas aplicadas.\nAumente o tamanho da viga ou remova as cargas que estão fora.")
                    return False
            
            desenha()


###################################
##Função Main - Interface Gráfica##
###################################
main = Tk()
main.title("Mecanica dos solidos 1 - Diagrama de momentos")
resource1 = resource_filename(__name__, 'favicon.ico')
main.iconbitmap(resource1)

#dimensoes da area de desenho
wc=450
hc=300

#Menu
menubar = Menu(main)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Sobre", command=lambda: messagebox.showinfo(title="Info", message="Programa para cálculo do momento fletor, força cortante e normal em uma viga biapoiada.\n\
Desenvolvido em Python e interface gráfica feita com a biblioteca tkinter.\n\n\
Mecanica dos Solidos 1 - 2º Semestre de 2023\n\
Professor Honorato\n\n\
Alunos:\n\
Thayná\n\
Ulisses Sebastian Ziech - 222026770"))

menubar.add_cascade(label="Ajuda", menu=helpmenu)
main.config(menu=menubar)

frame = Frame(main)
frame.pack()
frame_qp = LabelFrame(frame, text="Cargas Pontuais")
frame_qd = LabelFrame(frame, text="Cargas Distribuidas")
frame_remover_cargas = LabelFrame(frame, text="Remover Cargas")
frame_apoios = LabelFrame(frame, text="Pontos de apoio")
frame_etc = LabelFrame(frame, text="")
frame_grafico = LabelFrame(frame, text="")

frame_qp.grid(row=0, column=0, sticky="news", padx=10)
frame_qd.grid(row=2, column=0, sticky="news", padx=10)
frame_remover_cargas.grid(row=4, column=0, sticky="news", padx=10)
frame_apoios.grid(row=6, column=0, sticky="news", padx=10)
frame_etc.grid(row=8, column=0, sticky="news", padx=10)
frame_grafico.grid(row=0, column=6, sticky="news", padx=10, pady=10,rowspan=11)


#Inicia as variaveis de texto
# info1=Label(main, text="Forneça apenas valores numéricos com separador decimal sendo o ponto.")
# info2 = Label(main, text="Distância entre os pontos de apoio em metros.")
# info3 = Label(main, text="", font="Arial", fg="red")

#Carga pontual

qp=[]

qpfx_default = StringVar()
qpfy_default = StringVar()
qpxi_default = StringVar()

qpfx_default.set("0.00")
qpfy_default.set("0.00")
qpxi_default.set("0.00")

qpfx_entry = Entry(frame_qp, width=10, textvariable=qpfx_default)
qpfy_entry = Entry(frame_qp, width=10, textvariable=qpfy_default)
qpxi_entry = Entry(frame_qp, width=10, textvariable=qpxi_default)

texto_qp=Label(frame_qp, text="Carga:")
texto_qp_fxi=Label(frame_qp, text="Fxi (N)")
texto_qp_fyi=Label(frame_qp, text="Fyi (N)")
texto_qp_xi=Label(frame_qp, text="Coordenada Xi")

texto_qp.grid(row=1, column=0, padx=5, pady=5)
texto_qp_fxi.grid(row=0, column=1, padx=5, pady=5)
texto_qp_fyi.grid(row=0, column=2, padx=5, pady=5)
texto_qp_xi.grid(row=0, column=3, padx=5, pady=5)

qpfx_entry.grid(row=1, column=1, padx=5, pady=5)
qpfy_entry.grid(row=1, column=2, padx=5, pady=5)
qpxi_entry.grid(row=1, column=3, padx=5, pady=5)

botao_insere_qp = Button(frame_qp, text="Inserir", command=lambda: valida_entrada("qp",qp))
botao_insere_qp.grid(column=5, row=1, padx=10, pady=10)


#Carga distribuida

qd=[]

qdfx_default = StringVar()
qdfy_default = StringVar()
qdxi_default = StringVar()
qdxf_default = StringVar()
qdfx_default.set("0.00")
qdfy_default.set("0.00")
qdxi_default.set("0.00")
qdxf_default.set("0.00")

qdfx_entry = Entry(frame_qd, width=10, textvariable=qdfx_default)
qdfy_entry = Entry(frame_qd, width=10, textvariable=qdfy_default)
qdxi_entry = Entry(frame_qd, width=10, textvariable=qdxi_default)
qdxf_entry = Entry(frame_qd, width=10, textvariable=qdxf_default)

texto_qd=Label(frame_qd, text="Carga:")
texto_qd_fxi=Label(frame_qd, text="Fxi (N)")
texto_qd_fyi=Label(frame_qd, text="Fyi (N)")
texto_qd_xi=Label(frame_qd, text="X inicial")
texto_qd_xf=Label(frame_qd, text="X final")

texto_qd.grid(row=3, column=0)
texto_qd_fxi.grid(row=2, column=1, padx=5, pady=5)
texto_qd_fyi.grid(row=2, column=2, padx=5, pady=5)
texto_qd_xi.grid(row=2, column=3, padx=5, pady=5)
texto_qd_xf.grid(row=2, column=4, padx=5, pady=5)

qdfx_entry.grid(row=3, column=1, padx=5, pady=5)
qdfy_entry.grid(row=3, column=2, padx=5, pady=5)
qdxi_entry.grid(row=3, column=3, padx=5, pady=5)
qdxf_entry.grid(row=3, column=4, padx=5, pady=5)

botao_insere_qd = Button(frame_qd, text="Inserir", command=lambda: valida_entrada("qd",qd))
botao_insere_qd.grid(column=5, row=3, padx=10, pady=10)

#Remover carga
texto_remover=Label(frame_remover_cargas, text="Carga número:")
texto_remover.grid(row=4,column=0)

carga_default = StringVar()
carga_default.set("1")
carga_tipo_default = StringVar()
carga_tipo_default.set("Carga pontual")

carga_entry = Entry(frame_remover_cargas,width=10, textvariable=carga_default)
carga_entry.grid(row=4, column=1)

combobox = ttk.Combobox(frame_remover_cargas,state="readonly",values=["Carga pontual", "Carga Distribuida"], textvariable=carga_tipo_default)
combobox.grid(row=4,column=2, padx=10, pady=10)

botao_remover = Button(frame_remover_cargas, text="Remover", command=lambda: valida_entrada("remover",qd))
botao_remover.grid(column=5, row=4, padx=10, pady=10)

#Apoios
coord_ex_default = StringVar()
coord_dx_default = StringVar()
coord_ex_default.set("0.00")
coord_dx_default.set("2.00")

coord_ex_entry = Entry(frame_apoios, width=10, textvariable=coord_ex_default)
coord_dx_entry = Entry(frame_apoios, width=10, textvariable=coord_dx_default)

texto_apoio_e=Label(frame_apoios, text="Apoio esquerdo (m):")
texto_apoio_d=Label(frame_apoios, text="Apoio direito (m)")
texto_apoio_e.grid(row=5, column=0, padx=5, pady=5)
texto_apoio_d.grid(row=5, column=3, padx=5, pady=5)

coord_ex_entry.grid(row=5, column=1, padx=5, pady=5)
coord_dx_entry.grid(row=5, column=4, padx=5, pady=5)

botao_insere_apoio = Button(frame_apoios, text="Inserir", command=lambda: valida_entrada("apoio",qd))
botao_insere_apoio.grid(column=5, row=5, padx=10, pady=10)

#Frame ETC
botao_calcular = Button(frame_etc, text="Calcular", command=valida_entrada)
botao_calcular.grid(column=1, row=7, padx=10, pady=10)

botao_sair = Button(master=frame_etc, text="Sair", command=main.destroy)
botao_sair.grid(column=2, row=7, padx=10, pady=10)

relacao_qp=Label(frame_etc, textvariable="")
relacao_qp.grid(column=0, row=8, padx=10, pady=10)

relacao_qd=Label(frame_etc, text="")
relacao_qd.grid(column=0, row=9, padx=10, pady=10)

#Frame grafico
#Tela de desenhos
canvas = Canvas(frame_grafico, width=wc, height=hc, bg="white")




main.mainloop()