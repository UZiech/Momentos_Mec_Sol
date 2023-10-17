from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pkg_resources import resource_filename

##############################
##Força de reação dos apoios##
##############################
def forca_reacao():

    yb=hc-hc/3
    yv=yb-22
    valor_dist=abs(float(coord_dx_entry.get())-float(coord_ex_entry.get()))
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    #se já tinha algo desenhado, armazena variavel para limpar tudo ao final
    if canvas.gettags("reacao"):
        canvas.delete("reacao")
        return False
    
    fex=0.0 #força resultante em x, no apoio esquerdo devido as cargas pontuais. Nao existira essa força no apoio direito, uma vez que é uma poio de 1º genero
    fey=0.0 #força resultante em y, no apoio esquerdo devido as cargas pontuais
    fdy=0.0 #força resultante em y, no apoio direito devido as cargas pontuais
    fexd=0.0 #força resultante em x, no apoio esquerdo devido as cargas distribuidas. Nao existira essa força no apoio direito, uma vez que é uma poio de 1º genero
    feyd=0.0  #força resultante em y, no apoio esquero devido as cargas distribuidas
    fdyd=0.0  #força resultante em y, no apoio direito devido as cargas distribuidas
    Frql=0.0 #força resultante em toda a extensao da forca distribuida
    soma_fdy=0.0 #somatorio da força distribuida em y, aplicada no ponto de efetiva aplicacao da forca distribuida
    soma_fdx=0.0 #somatorio da força distribuida em x, aplicada no ponto de efetiva aplicacao da forca distribuida


    valores_qdx = []
    valores_qdy = []
    valores_xiqd = []
    valores_xfqd = []

    valores_qpx = []
    valores_qpy = []
    valores_xiqp = []

    #coloca dentro das listas, apenas a força em x, em y, xi e xf que estão dentro da lista qd que são as cargas fornecidas pelo usuario
    for i in range(0,len(qd),4):
        valores_qdx.append(qd[i])
        valores_qdy.append(qd[i+1])
        valores_xiqd.append(qd[i+2])
        valores_xfqd.append(qd[i+3])

    #coloca dentro das listas, apenas a força em x, em y, xi e o x de atuação das cargas pontuais
    for i in range(0,len(qp),3):
        valores_qpx.append(qp[i])
        valores_qpy.append(qp[i+1])
        valores_xiqp.append(qp[i+2])
    
    #calcula o valor da força resultante devido às cargas distribuidas
    for i in range(len(valores_qdy)):
        dql=abs(valores_xfqd[i]-valores_xiqd[i]) #distancia pela qual há ação da carga distribuida
        Frql=float(valores_qdy[i]*dql)         #forca resultande em y devido a carga distribuida
        Frqlx=float(valores_qdx[i]*dql)         #forca resultande em x devido a carga distribuida
        soma_fdy=soma_fdy+Frql
        soma_fdx=soma_fdx+Frqlx        #a soma das forças em x devido as cargas distribuida pode ser colocado no loop das forças atuantes no eixo y, pois as listas de força em y e força em x tem a mesma dimensao
        xefql=valores_xiqd[i]+dql/2    #local efetivo de aplicacao da forca resultante da carga distribuida
        feyd=feyd-(valor_dist-xefql)*Frql  #somatorio dos momentos, devido a aplicacao das forca resultande no ponto de aplicacao da força, devido a carga distribuida

    feyd=feyd/valor_dist
    fdyd=-(feyd+soma_fdy)
    fexd=soma_fdx

    #Calculo do momento devido às cargas pontuais
    #somatorio dos momentos deve ser igual a zero. Fazendo em relação ao ponto direito e resolvendo para fey
    for j in range(len(valores_qpy)):

        #em caso de coordenadas negativas dos pontos de aplicação das forças, pega a distancia absoluta entre o ponto de aplicacao e o ponto do apoio. Caso contrario, pode ser utilizado o proprio ponto de aplicacao da forca
        if valores_xiqp[j] < 0:
            xi=abs(float(coord_ex_entry.get())-valores_xiqp[j])
            xih=abs(float(coord_ex_entry.get())-valores_xiqp[j]) #para desenhar os vetores horizontais

        else:
            xi=valores_xiqp[j]
            xih=valores_xiqp[j] #para desenhar os vetores horizontais

        fex = fex + valores_qpx[j]
        fey = fey+(valor_dist-xi)*valores_qpy[j]
        
    fey=-(fey/valor_dist)

    
    #somatorio das forças deve ser igual a zero. Considerando os dois pontos de apoio direito e esquerdo, com componentes x e y
    fdy= -(fey+sum(valores_qpy))


    fey=fey+feyd #fazendo fey ser a força resultante em y no apoio esquerdo (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.
    fdy=fdy+fdyd #fazendo fey ser a força resultante em y no apoio direito (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.
    fexr = -(fex + fexd) #fazendo fexr ser a força resultante em x no apoio esquerdo (somatorio das cargas distribuidas e pontuais)

    fey_text = str(f'{fey:.3f}') + "N"
    fdy_text = str(f'{fdy:.3f}') + "N"
    fexr_text = str(f'{fexr:.3f}') + "N"

    #esses ifs são para verificar se as forças são maiores que zero para desenhar no sentido correto
    # desenha a força resultante em x no apoio esquerdo  
    if fexr<0:
        canvas.create_polygon(x0,yv,x0+10, yv-10,x0+10,yv+10, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a direita
        canvas.create_line(x0,yv, x0+50, yv, fill="red", width=2,tags="reacao") 
        canvas.create_text(x0+45, yv+15, text=fexr_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")  #escreve o valor da força de reação
    elif fexr>0:
        canvas.create_polygon(x0,yv,x0-10, yv-10,x0-10,yv+10, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a esquerda
        canvas.create_line(x0,yv, x0-50, yv, fill="red", width=2,tags="reacao") 
        canvas.create_text(x0-45, yv+15, text=fexr_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")  #escreve o valor da força de reação


    # desenha a força resultante em y no apoio esquerdo  
    if fey<0:
        canvas.create_polygon(x0-10,yv-20,x0, yv,x0+10,yv-20, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a direita
        canvas.create_line(x0,yv-20, x0, yv-82, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+5, yv-95, text=fey_text, fill="black", font=('Helvetica 10 bold'),tag="reacao") #escreve o valor da força de reação
    elif fey>0:
        canvas.create_polygon(x0-10,yb,x0, yv,x0+10,yb, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a esquerda
        canvas.create_line(x0,yb, x0, yv+82, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+5, yv+95, text=fey_text, fill="black", font=('Helvetica 10 bold'),tag="reacao") #escreve o valor da força de reação
   
    # desenha a força resultante em y no apoio direito
    if fdy<0:
        canvas.create_polygon(x0+valor_dist*a-10,yv-20,x0+valor_dist*a, yv,x0+valor_dist*a+10,yv-20, outline="red", width = 2, fill="white",tag="reacao")
        canvas.create_line(x0+valor_dist*a,yv-20, x0+valor_dist*a, yv-82, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+valor_dist*a+5, yv-95, text=fdy_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")
    elif fdy>0:
        canvas.create_polygon(x0+valor_dist*a-10,yb,x0+valor_dist*a, yv,x0+valor_dist*a+10,yb, outline="red", width = 2, fill="white",tag="reacao")
        canvas.create_line(x0+valor_dist*a,yb, x0+valor_dist*a, yv+82, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+valor_dist*a+5, yv+95, text=fdy_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")     

####################################################################
##Função que habilita novas entradas, para permitir novos calculos##
####################################################################

def habilita_entradas(botao_novos_valores, botao_qp, botao_ql, botao_reacao):
    qpfx_entry.config(state="normal")
    qpfy_entry.config(state="normal")
    qpxi_entry.config(state="normal")

    qdfx_entry.config(state="normal")
    qdfy_entry.config(state="normal")
    qdxi_entry.config(state="normal")
    qdxf_entry.config(state="normal")

    coord_ex_entry.config(state="normal")
    coord_dx_entry.config(state="normal")

    carga_entry.config(state="normal")
    combobox.config(state="readonly")

    #retira os botoes que aparecem embaixo do grafico
    botao_novos_valores.grid_forget()
    canvas.delete("all")
    canvas.grid_forget()

    botao_sair.grid_forget()
    botao_qp.grid_forget()
    botao_ql.grid_forget()
    botao_reacao.grid_forget()
    frame_grafico.grid_forget()


    botao_insere_qp.grid(column=5, row=1, padx=10, pady=10)
    botao_insere_qd.grid(column=5, row=3, padx=10, pady=10)
    botao_remover.grid(column=5, row=4, padx=10, pady=10)
    botao_insere_apoio.grid(column=5, row=5, padx=10, pady=10)

######################################################################
##Função que desabilita novas entradas, para não confundir o usuario##
######################################################################

def desabilita_entradas(botao_qp, botao_ql, botao_reacao):
    qpfx_entry.config(state="disabled")
    qpfy_entry.config(state="disabled")
    qpxi_entry.config(state="disabled")

    qdfx_entry.config(state="disabled")
    qdfy_entry.config(state="disabled")
    qdxi_entry.config(state="disabled")
    qdxf_entry.config(state="disabled")
    coord_ex_entry.config(state="disabled")
    coord_dx_entry.config(state="disabled")

    carga_entry.config(state="disabled")
    combobox.config(state="disabled")

    botao_insere_qp.grid_forget()
    botao_insere_qd.grid_forget()
    botao_remover.grid_forget()
    botao_insere_apoio.grid_forget()
    
    #Inicialia o botao que permite inserir novos valores
    botao_novos_valores = Button(frame_grafico, text="Novos Valores", command=lambda: habilita_entradas(botao_novos_valores, botao_qp, botao_ql, botao_reacao))
    botao_novos_valores.grid(column=6, row=11, padx=10, pady=10)

##############################
##Desenha as cargas pontuais##
##############################
def desenha_qp():

    yb=hc-hc/3 #hc é definida na função princial, portanto, é a altura do canvas. yb é a base dos apoios
    yv=yb-22   #yv é a localização da barra
    valor_dist=float(coord_dx_entry.get())-float(coord_ex_entry.get())
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    #verifica se já tinha algo desenhado para poder apagar ao final
    if canvas.gettags("qp"):
        canvas.delete("qp")
        return False

    valores_qpx = []
    valores_qpy = []
    valores_xiqp = []

    #coloca dentro das listas, apenas a força em x, em y, xi e o x de atuação das cargas pontuais
    for i in range(0,len(qp),3):
        valores_qpx.append(qp[i])
        valores_qpy.append(qp[i+1])
        valores_xiqp.append(qp[i+2])
    
    for i in range(len(valores_qpy)):

        #em caso de coordenadas negativas das forças, faz a proporcionalidade para iniciar os desenhos em cima do ponto de apoio da esquerda
        if valores_xiqp[i] < 0:
            xi=abs(float(coord_ex_entry.get())-valores_xiqp[i])
            xih=abs(float(coord_ex_entry.get())-valores_xiqp[i]) #para desenhar os vetores horizontais

        else:
            xi=valores_xiqp[i]
            xih=valores_xiqp[i] #para desenhar os vetores horizontais

       
        #esses ifs são para verificar se as cargas pontuais são maiores que zero para desenhar a seta no sentido correto
        #desenha os vetores das forças em y
        if valores_qpy[i]<0:
            canvas.create_polygon(x0+xi*a-10,yv-10,x0+xi*a, yv,x0+xi*a+10,yv-10, outline="skyblue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xi*a,yv-10, x0+xi*a, yv-50, fill="skyblue", width=2,tags="qp")
        elif valores_qpy[i]>0:
            canvas.create_polygon(x0+xi*a-10,yv+10,x0+xi*a, yv,x0+xi*a+10,yv+10, outline="skyblue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xi*a,yv+10, x0+xi*a, yv+50, fill="skyblue", width=2,tags="qp")
        #desenha os vetores das forças em y
        if valores_qpx[i]<0:
            canvas.create_polygon(x0+xih*a+10 , yv-10 , x0+xih*a+10 , yv+10 , x0+xih*a, yv, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xih*a,yv, x0+xih*a+50, yv, fill="blue", width=2,tags="qp")
        elif valores_qpx[i]>0:
            canvas.create_polygon(x0+xih*a-10,yv-10,x0+xih*a-10, yv+10, x0+xih*a,yv, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xih*a,yv, x0+xih*a-50, yv, fill="blue", width=2,tags="qp")    

##################################
##Desenha as cargas distribuidas##
##################################
def desenha_qd():
  
    yb=hc-hc/3
    yv=yb-22
    valor_dist=abs(float(coord_dx_entry.get())-float(coord_ex_entry.get()))

    espacamento_vetores=50 #espaçamento entre vetores em pixel
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    valores_qdx = []
    valores_qdy = []
    valores_xiqd = []
    valores_xfqd = []

    #se já tinha algo desenhado, no final apaga tudo  
    if canvas.gettags("ql"):
        canvas.delete("ql")
        return False


    for i in range(0,len(qd),4):
        valores_qdx.append(qd[i])
        valores_qdy.append(qd[i+1])
        valores_xiqd.append(qd[i+2])
        valores_xfqd.append(qd[i+3])


    for v in range(0,len(valores_xiqd)):
        
        qtd_vetores = abs(int((valores_xfqd[v]*a-valores_xiqd[v]*a)/espacamento_vetores))

        #em caso de coordenadas negativas das forças, faz a proporcionalidade para iniciar os desenhos em cima do ponto de apoio da esquerda
        if valores_xiqd[v] < 0:
            xi=abs(float(coord_ex_entry.get())-valores_xiqd[v])
            xih=abs(float(coord_ex_entry.get())-valores_xiqd[v]) #para desenhar os vetores horizontais

            xa=xi #para poder usar como coordenada na hora de desenhar a linha que liga os vetores
        else:
            xi=valores_xiqd[v]
            xih=valores_xiqd[v] #para desenhar os vetores horizontais
            xa=xi #para poder usar como coordenada na hora de desenhar a linha que liga os vetores
            
    
        #Se a distancia final for muito proximo da inicial da carga distribuida, recaira em divisão por zero. Esse if é para evitar divisao por zero
        if qtd_vetores <= 1:
            qtd_vetores=1

        incremento=abs(float((valores_xfqd[v]-valores_xiqd[v])/(qtd_vetores))) #incremento para pula a coordenda x de vetor em vetor

        #cria os vetores de força em y devido a carga distribuida
        if valores_qdy[v] < 0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv-10,x0+xi*a, yv,x0+xi*a+5,yv-10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv-82, fill="green", width=2,tag="ql")
                xi=xi+incremento
                    
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+xa*a,yv-82, x0+(xi-incremento)*a, yv-82, fill="green", width=2,tag="ql")
        elif valores_qdy[v] >0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv+10,x0+xi*a, yv,x0+xi*a+5,yv+10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv+82, fill="green", width=2,tag="ql")
                xi=xi+incremento
                    
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+xa*a,yv+82, x0+(xi-incremento)*a, yv+82, fill="green", width=2,tag="ql")
      
        incremento=abs(float((valores_xfqd[v]-valores_xiqd[v])/(qtd_vetores))) #incremento para pula a coordenda x de vetor em vetor
       
        #cria os vetores de força em x devido a carga distribuida
        if valores_qdx[v] < 0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xih*a,yv, x0+xih*a+5, yv+5,x0+xih*a+5,yv-5, outline="green", width = 2, fill="white",tag="ql") #seta para a esquerda
                canvas.create_line(x0+xih*a+5,yv, x0+xih*a+50, yv, fill="green", width=2,tag="ql") #cabo do vetor para a direita
                xih=xih+incremento
                    
        elif valores_qdx[v] >0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xih*a,yv, x0+xih*a-5, yv+5, x0+xih*a-5,yv-5, outline="green", width = 2, fill="white",tag="ql") #seta para a direita
                canvas.create_line(x0+xih*a,yv, x0+xih*a-50, yv, fill="green", width=2,tag="ql") #cabo do vetor para a esquerda
                xih=xih+incremento                     

###########################################################################
##Função que mostra o grafico e e chama as funcoes que desenham as cargas##
###########################################################################
def desenha():
    #coordenadas de posicionamento do desenho
    yb=hc-hc/3 #coordenada da parte de baixo da base
    yv=yb-22 #coordenada vertical da barra
    xv=x0-12 #coordenada do ponto de apoio esquerdo na linha da viga(origem)
    valor_dist=float(coord_ex_entry.get())-float(coord_dx_entry.get())

    #Desenha os pontos de apoio - primeiro o da esquereda, depois o da direita e depois a viga
    #Desenho do apoio da esquerda - segundo genero
    canvas.create_polygon(xv, yb, xv+25, yb, xv+12, yv, outline="black", width = 2, fill="white")
    canvas.create_line(xv,yb+5,xv+5,yb)
    canvas.create_line(xv+5,yb+5,xv+10,yb)
    canvas.create_line(xv+10,yb+5,xv+15,yb)
    canvas.create_line(xv+15,yb+5,xv+20,yb)
    canvas.create_line(xv+20,yb+5,xv+25,yb)

    #Desenho do apoio da direita - movel
    canvas.create_polygon(xf-12, yb, xf+13, yb, xf, yv, outline="black", width = 2, fill="white")
    canvas.create_oval(xf-12, yb+5, xf-7, yb, fill="white")
    canvas.create_oval(xf-7, yb+5, xf-2, yb, fill="white")
    canvas.create_oval(xf-2, yb+5, xf+3, yb, fill="white")
    canvas.create_oval(xf+3, yb+5, xf+8, yb, fill="white")
    canvas.create_oval(xf+8, yb+5, xf+13, yb, fill="white")
    canvas.create_line(xf-15,yb+5,xf+16,yb+5)       #linha da base de suporte do ponto de apoio da direita
    canvas.create_line(xf-17,yb+10,xf-12,yb+5)
    canvas.create_line(xf-10,yb+10,xf-5,yb+5)
    canvas.create_line(xf-5,yb+10,xf,yb+5)
    canvas.create_line(xf,yb+10,xf+5,yb+5)
    canvas.create_line(xf+5,yb+10,xf+10,yb+5)
    canvas.create_line(xf+10,yb+11,xf+16,yb+5)

    #Desenho da viga
    canvas.create_line(x0, yv, xf, yv, width = 4, fill="black")    
    
    #Dispões o gráfco no grid
    canvas.grid(column=6, row=0, padx=10, pady=10, rowspan=10,columnspan=3)
    
    #Inicializa e mostra os botoes que irao chamar as funções para exibir as cargas pontuais ou distribuida
    botao_qp = Button(frame_grafico, text="Cargas Pontuais", command=desenha_qp)
    botao_qd = Button(frame_grafico, text="Cargas Distribuidas", command=desenha_qd)
    botao_reacao = Button(frame_grafico, text="Reação", command=forca_reacao)
    frame_grafico.grid(row=0, column=6, sticky="news", padx=10, pady=10,rowspan=11)
    botao_qp.grid(column=6, row=10, padx=10, pady=10)
    botao_qd.grid(column=7, row=10, padx=10, pady=10)
    botao_reacao.grid(column=8, row=10, padx=10, pady=10)
    botao_sair.grid(column=8, row=11, padx=10, pady=10)

    return botao_qp, botao_qd, botao_reacao

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
            
            if float(qdxi_entry.get()) > float(qdxf_entry.get()):
                messagebox.showerror(title="Info", message="Corrigir as coordenadas de início e fim da carga aplicada.")
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

            botao_qp, botao_ql, botao_reacao = desenha()    
            desabilita_entradas(botao_qp, botao_ql, botao_reacao)
            
###################################
##Função Main - Interface Gráfica##
###################################
main = Tk()
main.title("Mecanica dos solidos 1 - Diagrama de momentos")
resource1 = resource_filename(__name__, 'favicon.ico')
main.iconbitmap(resource1)

#dimensoes da area de desenho
wc=500
hc=300

#margem esquerda e direita no grafico para inicio dos desenhos
x0=60
xf=440

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

#inicializa e distribui os diversos frames. Conforme forem sendo inseridos os widgets dentro dos frames eles vão aparecendo na interface gráfica
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
texto_qd_fxi=Label(frame_qd, text="Fxi (N/m)")
texto_qd_fyi=Label(frame_qd, text="Fyi (N/m)")
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

botao_insere_apoio = Button(frame_apoios, text="Desenhar viga", command=lambda: valida_entrada("apoio",qd))
botao_insere_apoio.grid(column=5, row=5, padx=10, pady=10)

#Frame ETC. Nesse frame que serão listadas as cargas que forem sendo adicionadas - funções envolvidas: listar_cargas que é chamada pelas funcoes remover_cargas ou valida_entrada
relacao_qp=Label(frame_etc, textvariable="")
relacao_qp.grid(column=0, row=8, padx=10, pady=10)

relacao_qd=Label(frame_etc, text="")
relacao_qd.grid(column=0, row=9, padx=10, pady=10)

#Frame grafico
#Tela de desenhos
canvas = Canvas(frame_grafico, width=wc, height=hc, bg="white")

botao_sair = Button(master=frame_grafico, text="Sair", command=main.destroy)


main.mainloop()