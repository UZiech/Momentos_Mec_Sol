from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pkg_resources import resource_filename

###########################
##Diagrama forca cortante##
###########################
def diagrama_cortante():
    yb=140
    yv=yb-60
    valor_dist=abs(float(coord_dx_entry.get())-float(coord_ex_entry.get()))
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    fey=0.0 #força resultante em y, no apoio esquerdo devido as cargas pontuais
    fdy=0.0 #força resultante em y, no apoio direito devido as cargas pontuais
    feyd=0.0  #força resultante em y, no apoio esquero devido as cargas distribuidas
    fdyd=0.0  #força resultante em y, no apoio direito devido as cargas distribuidas
    Frql=0.0 #força resultante em toda a extensao da forca distribuida
    soma_fdy=0.0 #somatorio da força distribuida em y, aplicada no ponto de efetiva aplicacao da forca distribuida

    valores_qdy = []
    valores_xiqd = []
    valores_xfqd = []

    valores_qpy = []
    valores_xiqp = []
    qpy = []

    #se já tinha algo desenhado, apaga e não faz mais nada
    if canvas.gettags("cortante"):
        canvas.delete("cortante")
        return False

    #coloca dentro das listas, apenas a força em y, xi e xf que estão dentro da lista qd que são as cargas fornecidas pelo usuario
    for i in range(0,len(qd),4):
        valores_qdy.append(qd[i+1])
        valores_xiqd.append(qd[i+2])
        valores_xfqd.append(qd[i+3])

    #coloca dentro das listas, apenas a força em y, xi e o x de atuação das cargas pontuais
    for i in range(0,len(qp),3):
        valores_qpy.append(qp[i+1])
        valores_xiqp.append(qp[i+2])
    
    #calcula o valor da força resultante devido às cargas distribuidas
    for i in range(len(valores_qdy)):
        dql=abs(valores_xfqd[i]-valores_xiqd[i]) #distancia pela qual há ação da carga distribuida
        Frql=float(valores_qdy[i]*dql)         #forca resultande em y devido a carga distribuida
        soma_fdy=soma_fdy+Frql
        xefql=valores_xiqd[i]+dql/2    #local efetivo de aplicacao da forca resultante da carga distribuida
        feyd=feyd-(valor_dist-abs(float(coord_ex_entry.get())-xefql))*Frql  #somatorio dos momentos, devido a aplicacao das forca resultande no ponto de aplicacao da força, devido a carga distribuida

    feyd=(feyd/valor_dist)
    fdyd=-(feyd+soma_fdy)


    #Calculo do momento devido às cargas pontuais
    #somatorio dos momentos deve ser igual a zero. Fazendo em relação ao ponto direito e resolvendo para fey
    for j in range(len(valores_qpy)):

        #acha a distancia entre a coordenada do ponto de apoio esquerdo (utilizado como origem para fazer os desenhos) e o ponto de aplicação da força.
        # xi=abs(float(coord_ex_entry.get())-valores_xiqp[j])
        # fey = fey+(valor_dist-xi)*valores_qpy[j]


        ##################problema a ser resolvido - Quando a força é aplicada exatamente sobre os pontos de apoio, não deveria ter força cortante
        if (round(valores_xiqp[j],2) != round(float(coord_ex_entry.get()),2)) and (round(valores_xiqp[j],2) != round(float(coord_dx_entry.get()),2)):
            #fey1 = fey - (valor_dist-xi)*valores_qpy[j]
            xi=abs(float(coord_ex_entry.get())-valores_xiqp[j])
            fey = fey+(valor_dist-xi)*valores_qpy[j]
    
        
    fey=-(fey/valor_dist)   
    #somatorio das forças deve ser igual a zero. Considerando os dois pontos de apoio direito e esquerdo, com componentes x e y
    fdy= -(fey+sum(valores_qpy))


    freacao_e=fey+feyd 
    freacao_d=fdy+fdyd
    fcortante_e = freacao_e
    cortante = freacao_e
    maior_cortante = cortante

    #se não tiver força de reação nos apoios, significa que não tem carga vertical liquida
    if (freacao_e == 0) and (freacao_d == 0):
        canvas.create_line(x0,yv-50, xf, yv-50, dash=(10,10), tags="cortante")
        canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="cortante")
        canvas.create_text(x0, yv-33, text="Não há cargas verticais líquidas nos pontos de apoio.", anchor="w", fill="red", font=('Helvetica 10 bold'),tag="cortante")
        canvas.create_text(x0, yv-17, text="Este programa não calcula vigas hiperestáticas.", anchor="w", fill="red", font=('Helvetica 10 bold'),tag="cortante")
        canvas.create_text(x0-20, yv-60, text="Diagrama de esforço cortante", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="cortante")  
        return False

    #Desenha as linhas de base do diagrama e insere o texto informativo
    canvas.create_line(x0,yv-50, xf, yv-50, dash=(10,10), tags="cortante")
    canvas.create_line(x0,yv-25, xf, yv-25, tags="cortante")
    canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="cortante")
    canvas.create_text(x0-20, yv-60, text="Diagrama de esforço cortante", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="cortante")  
    
    #transforma as cargas distribuidas em cargas pontuais, colocando as cargas dentro da lista de cargas pontuais e as posições de ação das cargas dentro da lista de posicao de ação das cargas pontuais
    qpy=valores_qpy
    qdy=valores_qdy
    xiqp = valores_xiqp
    xiqd=valores_xiqd
    xfqd=valores_xfqd

    for i in range(len(qdy)):
        incremento = 0.01
        pos = xiqd[i]

        while (pos<=xfqd[i]):
            qpy.append(qdy[i]*incremento)
            xiqp.append(pos+incremento/2)
            pos=pos+incremento

    #ordena as listas de força e posicao com base na ordem crescrente da posicao
    indices = list(range(len(xiqp)))
    indices.sort(key=lambda i: xiqp[i])

    qpy = [qpy[i] for i in indices]
    xiqp = [xiqp[i] for i in indices]

    ############
    #Descobre o maior valor da forca cortante, para entao comparar com as forcas nos pontos de apoio e poder desenhar o diagrama dentro dos limites
    for i in range(len(qpy)): #qpy são todas as cargas, inclusive as distribuidas que foram transformadas em pontuais e estão em ordenadas de acordo com a posicao

        ###########problema. atentar que coloquei esse if. A ideia é só contribuir para a alteração da força cortante se nao for carga sobre os apoios
        if round(xiqp[i],2) != round(float(coord_ex_entry.get()),2) and round(xiqp[i],2) != round(float(coord_dx_entry.get()),2):
            cortante = qpy[i]+cortante

        if abs(cortante)>abs(maior_cortante):
            maior_cortante=cortante

    # proporcao para fazer o desenho do diagrama e sempre considerar a maior forca como o ponto maximo do desenho
    b = 25/abs(max(abs(freacao_e),abs(freacao_d),abs(maior_cortante)))


    #Calcula as forças cortantes devido a cada uma das cargas e cria a lista par ordenado para desenhar o diagrama
    par_coordenado = [x0,yv-25,x0,yv-25-fcortante_e*b] #coordenadas do ponto de apoio esquedo e da primeira força cortante
    for i in list(range(len(qpy))):
        xi=abs(float(coord_ex_entry.get())-xiqp[i])

        par_coordenado.append(x0+xi*a)
        par_coordenado.append(yv-25-fcortante_e*b)
        
        if round(xiqp[i],2) != round(float(coord_ex_entry.get()),2) and round(xiqp[i],2) != round(float(coord_dx_entry.get()),2):
            fcortante_e = qpy[i]+fcortante_e

        par_coordenado.append(x0+xi*a)
        par_coordenado.append(yv-25-fcortante_e*b)
    
    par_coordenado.append(xf)
    par_coordenado.append(yv-25-fcortante_e*b)
    par_coordenado.append(xf)
    par_coordenado.append(yv-25)

    #desenha o diagrama
    canvas.create_line(par_coordenado,  fill="red", width=2,tags="cortante")

    #Apresenta os valores máximo e mínimo da força cortante
    cortante_text = str(f'{max(abs(freacao_e),abs(freacao_d),abs(maior_cortante)):.2f}') + "N"
    canvas.create_text(xf+5, yv-50, text=cortante_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="cortante")  #escreve o valor da cortante maxima na linha superior
    cortante_text = "-" + str(f'{max(abs(freacao_e),abs(freacao_d),abs(maior_cortante)):.2f}') + "N"
    canvas.create_text(xf+5, yv, text=cortante_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="cortante")  #escreve o valor da cortante minima na linha inferior

###########################
##Diagrama momento fletor##
###########################
def diagrama_momento_fletor():
    yb=240
    yv=yb-30
    valor_dist=abs(float(coord_dx_entry.get())-float(coord_ex_entry.get()))
    coord_ap_e = float(coord_ex_entry.get())
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    valores_qdy = []
    valores_xiqd = []
    valores_xfqd = []
    qdy = []
    xqdy = []

    valores_qpy = []
    valores_xiqp = []

    mfletor = []
    par_coordenado = []
    

    #se já tinha algo desenhado, apaga e não faz mais nada
    if canvas.gettags("fletor"):
        canvas.delete("fletor")
        return False

    #coloca dentro das listas, apenas a força em y, xi e xf que estão dentro da lista qd que são as cargas com as posicoes iniciais e finais, fornecidas pelo usuario
    for i in range(0,len(qd),4):
        valores_qdy.append(qd[i+1])
        valores_xiqd.append(qd[i+2])
        valores_xfqd.append(qd[i+3])

    #coloca dentro das listas, apenas a força em y, xi e o x de atuação das cargas pontuais
    for i in range(0,len(qp),3):
        valores_qpy.append(qp[i+1])
        valores_xiqp.append(qp[i+2])
    
#########################################################################Calculo da reacao nos pontos de apoio,                                    ######################### 
######################################################################                              começa aqui                                    #########################
    fey=0.0 #força resultante em y, no apoio esquerdo devido as cargas pontuais
    fdy=0.0 #força resultante em y, no apoio direito devido as cargas pontuais
    feyd=0.0  #força resultante em y, no apoio esquero devido as cargas distribuidas
    fdyd=0.0  #força resultante em y, no apoio direito devido as cargas distribuidas
    Frql=0.0 #força resultante em toda a extensao da forca distribuida
    soma_fdy=0.0 #somatorio da força distribuida em y, aplicada no ponto de efetiva aplicacao da forca distribuida
    
    #calcula o valor da força resultante devido às cargas distribuidas
    for i in range(len(valores_qdy)):
        dql=abs(valores_xfqd[i]-valores_xiqd[i]) #distancia pela qual há ação da carga distribuida
        Frql=float(valores_qdy[i]*dql)         #forca resultande em y devido a carga distribuida
        soma_fdy=soma_fdy+Frql
        xefql=valores_xiqd[i]+dql/2    #local efetivo de aplicacao da forca resultante da carga distribuida
        feyd=feyd-(valor_dist-abs(coord_ap_e-xefql))*Frql  #somatorio dos momentos, devido a aplicacao das forca resultande no ponto de aplicacao da força, devido a carga distribuida

    feyd=(feyd/valor_dist)
    fdyd=-(feyd+soma_fdy)


    #Calculo do momento devido às cargas pontuais
    #somatorio dos momentos deve ser igual a zero. Fazendo em relação ao ponto direito e resolvendo para fey
    for j in range(len(valores_qpy)):
        if (round(valores_xiqp[j],2) != round(coord_ap_e,2)) and (round(valores_xiqp[j],2) != round(float(coord_dx_entry.get()),2)):
            #acha a distancia entre a coordenada do ponto de apoio esquerdo (utilizado como origem para fazer os desenhos) e o ponto de aplicação da força.
            xi=abs(coord_ap_e-valores_xiqp[j])
            fey = fey+(valor_dist-xi)*valores_qpy[j]
    
        
    fey=-(fey/valor_dist)   
    #somatorio das forças deve ser igual a zero. Considerando os dois pontos de apoio direito e esquerdo, com componentes x e y
    fdy= -(fey+sum(valores_qpy))

    fey=fey+feyd #fazendo fey ser a força resultante em y no apoio esquerdo (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.
    fdy=fdy+fdyd #fazendo fey ser a força resultante em y no apoio direito (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.


    ################################################################################Calculo da reacao acaba aqui##################################################################


    #ordena as listas de carga pontual e posicao com base na ordem crescente da posicao
    xiqp = valores_xiqp

    indices = list(range(len(xiqp)))
    indices.sort(key=lambda i: xiqp[i])
    valores_qpy = [valores_qpy[i] for i in indices]
    xiqp = [xiqp[i] for i in indices]

    #transforma as cargas distribuidas em cargas pontuais
    incremento = 0.01
    for i in range(len(valores_qdy)):
        pos = valores_xiqd[i]

        while (pos<=valores_xfqd[i]):
            qdy.append(valores_qdy[i]*incremento)
            xqdy.append(pos)
            pos=round(pos+incremento,2)

    #calcula os momentos devidos as cargas pontuais e distribuidas ao longo de todo o comprimento da viga, integrando a posicao com incremento de 0.01
    pos=round(coord_ap_e,2)
    mfletor_local=0.0
    mfletor_local1=0.0
    mfletor1=[]
    xiqp1=[]

    #Calcula os momentos quando se tem apenas cargas pontuais
    if len(valores_qpy)>0 and len(valores_qdy)==0:
        while (pos<=float(coord_dx_entry.get())):
            mfletor_local=0.0
            for i in range(len(valores_qpy)): #qpy são apenas as cargas pontuais
                #problema. Colocando esse if, parte se resolve
                #if (pos == xiqp[i]):
                if (pos == coord_ap_e) or (pos == round(float(coord_dx_entry.get()),2)):
                    mfletor.append(0)


                #problema a ser resolvido. O momento fletor quando se tem apenas cargas pontuais não está calculando corretamente
                elif pos>=round(xiqp[i],2) and pos != coord_ap_e and pos != round(float(coord_dx_entry.get()),2):
                    # mfletor_local = (valores_qpy[i]*abs(coord_ap_e-xiqp[i])) + mfletor_local
                    # mfletor.append(mfletor_local + fey*abs(coord_ap_e - xiqp[i]))
                    mfletor_local = (valores_qpy[i]*abs(pos-xiqp[i])) + mfletor_local
                    mfletor.append(mfletor_local+ fey*abs(coord_ap_e - xiqp[i]))


            pos=round(pos+incremento,2)

    #Calcula os momentos quando se tem apenas cargas distribuidas
    if len(valores_qpy)==0 and len(valores_qdy)>0:
        while (pos<=float(coord_dx_entry.get())):
            mfletor_local=0.0
            for i in range(len(qdy)): #qdy são as cargas distribuidas que foram transformadas em pontuais
                if (pos == xqdy[i]):
                    mfletor_local = (valores_qdy[0])*(abs(valores_xiqd[0]-xqdy[i]))*abs(valores_xiqd[0]-xqdy[i])/2 
                    mfletor.append((mfletor_local + fey*abs(coord_ap_e - xqdy[i])))
                    xiqp.append(xqdy[i])
            pos=round(pos+incremento,2)

    #Calcula os momentos quando se tem cargas distribuidas e pontuais
    if len(valores_qpy)>0 and len(valores_qdy)>0:
        #integra a posicao ao longo de toda a viga
        while (pos<=float(coord_dx_entry.get())):

            #faz os calculos para todas as cargas pontuais. Nesse programa, somente uma carga distribuida é aceita na entrada dos dados.
            for i in range(len(valores_qpy)): 

                ###############Antes da carga distribuida
                # verifica se o local da integracao no comprimento da barra, está antes da carga distribuida
                if (pos < valores_xiqd[0]):

                    # verifica se no local da integracao no comprimento da barra, existe carga pontual
                    if (pos == xiqp[i]): 
                        mfletor_local = (valores_qpy[i]*abs(pos-xiqp[i])) + mfletor_local
                        mfletor.append(mfletor_local+ fey*abs(coord_ap_e - xiqp[i]))

                ###############Entre a ação da carga distribuida
                #verifica se o local da integracao no comprimento da barra, está entre a ação da carga distribuida
                elif (pos >= valores_xiqd[0]) and (pos <= valores_xfqd[0]):
                    
                    mfletor_local1=0.0
                    for k in range(len(xiqp)):
                        if xiqp[k]<pos:
                            mfletor_local1=(valores_qpy[k]*abs(pos-xiqp[k])) + mfletor_local1
                    
                    if (pos == xiqp[i]):
                        mfletor_dist = (valores_qdy[0])*(abs(valores_xiqd[0]-pos))*abs(valores_xiqd[0]-pos)/2
                        mfletor.append(mfletor_dist + fey*abs(coord_ap_e - pos) + mfletor_local1)

                    else:
                        mfletor_dist = (valores_qdy[0])*(abs(valores_xiqd[0]-pos))*abs(valores_xiqd[0]-pos)/2
                        mfletor1.append(mfletor_dist + fey*abs(coord_ap_e - pos) + mfletor_local1)
                        xiqp1.append(pos)


                ###############Após a ação da carga distribuida
                #verifica se o local da integracao no comprimento da barra, está após a ação da carga distribuida
                elif (pos > valores_xfqd[0]):
                    mfletor_local2=0.0

                    if (pos == xiqp[i]):
                        #mfletor_local = (valores_qpy[i]*abs(coord_ap_e-pos)) +valores_qdy[0]*abs(valores_xfqd[0]-valores_xiqd[0])*abs(((valores_xfqd[0]-valores_xiqd[0])/2)-pos) +mfletor_local
                        for k in range(len(xiqp)):
                            if xiqp[k]<pos:
                                mfletor_local2=(valores_qpy[k]*abs(pos-xiqp[k])) + mfletor_local2

                        #mfletor_local = (valores_qpy[i]*abs(coord_ap_e-pos))
                        mfletor_dist = valores_qdy[0]*abs(valores_xfqd[0]-valores_xiqd[0]) * (abs(pos - (abs(valores_xiqd[0]-valores_xfqd[0])/2 + valores_xiqd[0])))
                        mfletor.append(mfletor_local2 + fey*abs(coord_ap_e - pos) + mfletor_dist)

            pos=round(pos+incremento,2)

        #mfletor1 é uma lista auxiliar necessaria quando se tem carga pontual sobreposta com carga distribuida
        for j in range(len(mfletor1)):
            mfletor.append((mfletor1[j]))
            xiqp.append(xiqp1[j])

    #se não tiver momento fletor, não existe diagrama do momento fletor
    if max(list(map(abs,mfletor))) == 0.0:
        canvas.create_line(x0,yv-100, xf, yv-100, dash=(10,10), tags="fletor")
        canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="fletor")
        canvas.create_text(x0, yv-50, text="Não há momento fletor na viga.", anchor="w", fill="red", font=('Helvetica 10 bold'),tag="fletor")
        canvas.create_text(x0-20, yv-110, text="Diagrama do momento fletor", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="fletor")  
        return False

    # proporcao para fazer o desenho do diagrama e sempre considerar o maior momento como o ponto maximo/minimo do desenho
    b = 50/max(list(map(abs,mfletor)))

    #Desenha as linhas de base do diagrama e insere o texto informativo
    canvas.create_line(x0,yv-100, xf, yv-100, dash=(10,10), tags="fletor")
    canvas.create_line(x0,yv-50, xf, yv-50, tags="fletor")
    canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="fletor")
    canvas.create_text(x0-20, yv-110, text="Diagrama do momento fletor", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="fletor")

    #Apresenta os valores máximo e mínimo do momento fletor
    canvas_text = str(f'{max(list(map(abs,mfletor))):.2f}') + "N"
    canvas.create_text(xf+5, yv-100, text=canvas_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="fletor")  #escreve o valor do momento fletor máximo
    canvas_text = "-" + str(f'{max(list(map(abs,mfletor))):.2f}') + "N"    
    canvas.create_text(xf+5, yv, text=canvas_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="fletor")  #escreve o valor do momento fletor mínimo

    #multiplica cada elemento do eixo y (momento fletor) pela proporcionalidade b, de forma que fique dentro das linhas do diagrama
    mfletor = [(yv-50+j*b) for j in mfletor] 

    #ordena as listas de momento e posicao com base na ordem crescente da posicao
    indices = list(range(len(xiqp)))
    indices.sort(key=lambda i: xiqp[i])

    mfletor = [mfletor[i] for i in indices]
    xiqp = [xiqp[i] for i in indices]

    #insere na primeira e ultima posicao da lista do momento fletor e da posicao do momento fletor, as coordenadas e momento nos pontos de apoio
    mfletor.insert(0,yv-50)
    mfletor.append(yv-50)
    xiqp.insert(0,coord_ap_e)
    xiqp.append(float(coord_dx_entry.get()))



    #cria a lista par coordenado, com a posicao e o momento de todas as cargas e dos pontos de apoio
    for i in range(len(mfletor)):
        xi=abs(coord_ap_e-xiqp[i])
        par_coordenado.append(x0+xi*a)
        par_coordenado.append(mfletor[i])

    #Desenha o diagrama
    canvas.create_line(par_coordenado, fill="red", width=2,tags="fletor")

##############################
##Força de reação dos apoios##
##############################
def forca_reacao():

    yb=hc-y0
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
        feyd=feyd-(valor_dist-abs(float(coord_ex_entry.get())-xefql))*Frql  #somatorio dos momentos, devido a aplicacao das forca resultande no ponto de aplicacao da força, devido a carga distribuida

    feyd=(feyd/valor_dist)
    fdyd=-(feyd+soma_fdy)
    fexd=soma_fdx

    #Calculo do momento devido às cargas pontuais
    #somatorio dos momentos deve ser igual a zero. Fazendo em relação ao ponto direito e resolvendo para fey
    for j in range(len(valores_qpy)):

        #acha a distancia entre a coordenada do ponto de apoio esquerdo (utilizado como origem para fazer os desenhos) e o ponto de aplicação da força.
        xi=abs(float(coord_ex_entry.get())-valores_xiqp[j])
        fex = fex + valores_qpx[j]
        fey = fey+(valor_dist-xi)*valores_qpy[j]
        
    fey=-(fey/valor_dist)   
    #somatorio das forças deve ser igual a zero. Considerando os dois pontos de apoio direito e esquerdo, com componentes x e y
    fdy= -(fey+sum(valores_qpy))


    fey=fey+feyd #fazendo fey ser a força resultante em y no apoio esquerdo (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.
    fdy=fdy+fdyd #fazendo fey ser a força resultante em y no apoio direito (somatorio das cargas distribuidas e pontuais). O ideal seria uma outra variavel para facilitar a compreensão, mas aí precisaria editar o trecho do código que faz o desenho do gráfico, para fazer referencia à nova variavel.
    fexr = -(fex + fexd) #fazendo fexr ser a força resultante em x no apoio esquerdo (somatorio das cargas distribuidas e pontuais)

    if (fexr == 0.0) and (fdy == 0.0) and (fey == 0.0):
        canvas.create_text(x0, yv+55, text="Força de reação nos apoios é igual a zero.", fill="red", font=('Helvetica 10 bold'), anchor=W, tag="reacao")  #se não houver nenhum tipo de força de reação, não tem vetor, portanto, escreve que a força resultante nos apoios é igual a zero


    fey_text = str(f'{fey:.3f}') + "N"
    fdy_text = str(f'{fdy:.3f}') + "N"
    fexr_text = str(f'{fexr:.3f}') + "N"

    #esses ifs são para verificar se as forças são maiores que zero para desenhar no sentido correto
    # desenha a força resultante em x no apoio esquerdo. Não tem força resultante em x no ponto direito, pois o apoio é de 1º genero 
    if fexr<0:
        canvas.create_polygon(x0,yv,x0+10, yv-10,x0+10,yv+10, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a direita
        canvas.create_line(x0,yv, x0+50, yv, fill="red", width=2,tags="reacao") 
        canvas.create_text(x0+45, yv+15, text=fexr_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")  #escreve o valor da força de reação
    elif fexr>0:
        canvas.create_polygon(x0,yv,x0-10, yv-10,x0-10,yv+10, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a esquerda
        canvas.create_line(x0,yv, x0-50, yv, fill="red", width=2,tags="reacao") 
        canvas.create_text(x0-20, yv-15, text=fexr_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")  #escreve o valor da força de reação

    # desenha a força resultante em y no apoio esquerdo  
    if fey<0:
        canvas.create_polygon(x0-10,yv-20,x0, yv,x0+10,yv-20, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a direita
        canvas.create_line(x0,yv-20, x0, yv-50, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+5, yv-60, text=fey_text, fill="black", font=('Helvetica 10 bold'),tag="reacao") #escreve o valor da força de reação
    elif fey>0:
        canvas.create_polygon(x0-10,yb,x0, yv,x0+10,yb, outline="red", width = 2, fill="white",tag="reacao") #cria a seta para a esquerda
        canvas.create_line(x0,yb, x0, yv+50, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+5, yv+60, text=fey_text, fill="black", font=('Helvetica 10 bold'),tag="reacao") #escreve o valor da força de reação
   
    # desenha a força resultante em y no apoio direito
    if fdy<0:
        canvas.create_polygon(x0+valor_dist*a-10,yv-20,x0+valor_dist*a, yv,x0+valor_dist*a+10,yv-20, outline="red", width = 2, fill="white",tag="reacao")
        canvas.create_line(x0+valor_dist*a,yv-20, x0+valor_dist*a, yv-50, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+valor_dist*a+5, yv-60, text=fdy_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")
    elif fdy>0:
        canvas.create_polygon(x0+valor_dist*a-10,yb,x0+valor_dist*a, yv,x0+valor_dist*a+10,yb, outline="red", width = 2, fill="white",tag="reacao")
        canvas.create_line(x0+valor_dist*a,yb, x0+valor_dist*a, yv+50, fill="red", width=2,tags="reacao")
        canvas.create_text(x0+valor_dist*a+5, yv+60, text=fdy_text, fill="black", font=('Helvetica 10 bold'),tag="reacao")

#########################
##Diagrama força normal##
#########################
def diagrama_normal():
    yb=370
    yv=yb-30
    valor_dist=abs(float(coord_dx_entry.get())-float(coord_ex_entry.get()))
    coord_ap_e = float(coord_ex_entry.get())
    a=(xf-x0)/valor_dist #conversao proporcional ao valor fornecido para o comprimento da viga

    valores_qdx = []
    valores_xiqd = []
    valores_xfqd = []
    qpx = []
    normal=[]

    valores_qpx = []
    valores_xiqp = []

    par_coordenado = []
    

    #se já tinha algo desenhado, apaga e não faz mais nada
    if canvas.gettags("normal"):
        canvas.delete("normal")
        return False

    #coloca dentro das listas, apenas a força em x, xi e xf que estão dentro da lista qd que são as cargas com as posicoes iniciais e finais, fornecidas pelo usuario
    for i in range(0,len(qd),4):
        valores_qdx.append(qd[i])
        valores_xiqd.append(qd[i+2])
        valores_xfqd.append(qd[i+3])

    #coloca dentro das listas, apenas a força em x e o x de atuação das cargas pontuais
    for i in range(0,len(qp),3):
        valores_qpx.append(qp[i])
        valores_xiqp.append(qp[i+2])

    #transforma as cargas distribuidas em cargas pontuais, colocando os valores dentro da lista de carga pontual e das posicoes das cargas pontuais
    xiqp = valores_xiqp
    qpx = valores_qpx
    incremento = 0.01
    for i in range(len(valores_qdx)):
        pos = valores_xiqd[i]

        while (pos<valores_xfqd[i]):
            qpx.append(valores_qdx[i]*incremento)
            xiqp.append(pos)
            pos=round(pos+incremento,2)
    
    #Força de reação x no ponto de apoio esquerdo
    fexr = -sum(qpx)

    #ordena as listas de carga pontual e posicao com base na ordem crescente da posicao
    indices = list(range(len(xiqp)))
    indices.sort(key=lambda i: xiqp[i])
    #valores_qpx = [valores_qpx[i] for i in indices]
    qpx = [qpx[i] for i in indices]
    xiqp = [xiqp[i] for i in indices]

    #Calcula a forca em x, em cada local que possui carga
    somatorio_forca_x=fexr
    for i in range(len(xiqp)):
        somatorio_forca_x = qpx[i]+somatorio_forca_x
        normal.append(somatorio_forca_x)

    #se não tiver força no eixo x, não existe diagrama normal
    if (max(max(list(map(abs,normal))),abs(fexr)) == 0.0):
        canvas.create_line(x0,yv-100, xf, yv-100, dash=(10,10), tags="normal")
        canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="normal")
        canvas.create_text(x0, yv-50, text="Não há forças horizontais.", anchor="w", fill="red", font=('Helvetica 10 bold'),tag="normal")
        canvas.create_text(x0-20, yv-110, text="Diagrama da força normal", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="normal")  
        return False

    #ordena as listas de normal e posicao com base na ordem crescente da posicao
    indices = list(range(len(xiqp)))
    indices.sort(key=lambda i: xiqp[i])
    normal = [normal[i] for i in indices]
    xiqp = [xiqp[i] for i in indices]

    #Desenha as linhas de base do diagrama e insere o texto informativo
    canvas.create_line(x0,yv-100, xf, yv-100, dash=(10,10), tags="normal")
    canvas.create_line(x0,yv-50, xf, yv-50, tags="normal")
    canvas.create_line(x0,yv, xf, yv, dash=(10,10), tags="normal")
    canvas.create_text(x0-20, yv-110, text="Diagrama da força Normal", anchor="w", fill="black", font=('Helvetica 10 bold'),tag="normal")

    #Apresenta os valores máximo e mínimo da força normal
    canvas_text = str(f'{max(max(list(map(abs,normal))),abs(fexr)):.2f}') + "N"
    canvas.create_text(xf+5, yv-100, text=canvas_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="normal")  #escreve o valor do momento fletor máximo
    canvas_text = "-" + str(f'{max(max(list(map(abs,normal))),abs(fexr)):.2f}') + "N"    
    canvas.create_text(xf+5, yv, text=canvas_text, fill="black", anchor=W, font=('Helvetica 10 bold'),tag="normal")  #escreve o valor do momento fletor mínimo

    # proporcao para fazer o desenho do diagrama e sempre considerar a maior forca normal
    b = 50/(max(max(list(map(abs,normal))),abs(fexr)))

    #multiplica cada elemento do eixo y (força normal) pela proporcionalidade b, de forma que fique dentro das linhas do diagrama
    normal = [(yv-50+j*b) for j in normal] 

    #Cria a lista par ordenado para desenhar o diagrama
    # if fexr == 0.0:
    #     par_coordenado = [x0,yv-50,x0,normal[0]] #coordenadas do ponto de apoio esquedo e da primeira força normal
    # else:
    #     par_coordenado = [x0,yv-50,x0,yv-50-fexr*b] #coordenadas do ponto de apoio esquedo e da primeira força normal
    par_coordenado = [x0,yv-50,x0,yv-50+fexr*b,x0+a*abs(float(coord_ex_entry.get())-xiqp[0]), yv-50+fexr*b] #coordenadas do ponto de apoio esquerdo até a primeira carga
    #par_coordenado = [x0,yv-50,x0, normal[0],x0+a*abs(float(coord_ex_entry.get())-xiqp[0]), normal[0]] #coordenadas do ponto de apoio esquerdo até a primeira carga
    
    for i in list(range(len(qpx))):
        xi=abs(float(coord_ex_entry.get())-xiqp[i])

        if i == (len(qpx)-1): #se for a ultima carga, desce para o eixo x e segue até o final
            # par_coordenado.append(x0+xi*a)
            # par_coordenado.append(normal[i])
            par_coordenado.append(x0+xi*a)
            par_coordenado.append(yv-50)
            par_coordenado.append(xf)
            par_coordenado.append(yv-50)

        else: #se nao for a ultima carga, continua desenhando o diagrama
            xii=abs(float(coord_ex_entry.get())-xiqp[i+1])
            par_coordenado.append(x0+xi*a)
            par_coordenado.append(normal[i])
            par_coordenado.append(x0+xii*a)
            par_coordenado.append(normal[i])

    #Desenha o diagrama
    canvas.create_line(par_coordenado, fill="red", width=2,tags="normal")

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
    if len(qd) > 0:
        botao_insere_qd.grid_forget()
        qdfx_entry.config(state="disabled")
        qdfy_entry.config(state="disabled")
        qdxi_entry.config(state="disabled")
        qdxf_entry.config(state="disabled")

    elif (len(qd) == 0):
        botao_insere_qd.grid(column=5, row=3, padx=10, pady=10)
        qdfx_entry.config(state="normal")
        qdfy_entry.config(state="normal")
        qdxi_entry.config(state="normal")
        qdxf_entry.config(state="normal")
  
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
    botao_novos_valores.grid(column=6, row=10, padx=10, pady=10)

##############################
##Desenha as cargas pontuais##
##############################
def desenha_qp():

    yb=hc-y0 #hc é definida na função princial, portanto, é a altura do canvas. yb é a base dos apoios
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

        #acha a distancia entre a coordenada do ponto de apoio esquerdo (utilizado como origem para fazer os desenhos) e o ponto de aplicação da força. O calculo é usado para posicionar as forças em relação ao ponto de apoio
        xi=abs(float(coord_ex_entry.get())-valores_xiqp[i])
        xih=abs(float(coord_ex_entry.get())-valores_xiqp[i]) #para desenhar os vetores horizontais
     
        #esses ifs são para verificar se as cargas pontuais são maiores que zero para desenhar a seta no sentido correto
        #desenha os vetores das forças em y
        if valores_qpy[i]<0:
            canvas.create_polygon(x0+xi*a-10,yv-10,x0+xi*a, yv,x0+xi*a+10,yv-10, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xi*a,yv-10, x0+xi*a, yv-50, fill="blue", width=2,tags="qp")
        elif valores_qpy[i]>0:
            canvas.create_polygon(x0+xi*a-10,yv+10,x0+xi*a, yv,x0+xi*a+10,yv+10, outline="blue", width = 2, fill="white",tag="qp")
            canvas.create_line(x0+xi*a,yv+10, x0+xi*a, yv+50, fill="blue", width=2,tags="qp")
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
  
    yb=hc-y0
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

        #acha a distancia entre a coordenada do ponto de apoio esquerdo (utilizado como origem para fazer os desenhos) e o ponto de inicio de aplicação da força distribuida. O calculo é usado para posicionar as forças em relação ao ponto de apoio
        xi=abs(float(coord_ex_entry.get())-valores_xiqd[v])
        xih=abs(float(coord_ex_entry.get())-valores_xiqd[v]) #para desenhar os vetores horizontais
        xa=xi #para poder usar como coordenada na hora de desenhar a linha que liga os vetores            
    
        #Se a distancia final for muito proximo da inicial da carga distribuida, recaira em divisão por zero. Esse if é para evitar divisao por zero
        if qtd_vetores <= 1:
            qtd_vetores=1

        incremento=abs(float((valores_xfqd[v]-valores_xiqd[v])/(qtd_vetores))) #incremento para pula a coordenda x de vetor em vetor

        #cria os vetores de força em y devido a carga distribuida
        if valores_qdy[v] < 0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv-10,x0+xi*a, yv,x0+xi*a+5,yv-10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv-60, fill="green", width=2,tag="ql")
                xi=xi+incremento
                    
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+xa*a,yv-60, x0+(xi-incremento)*a, yv-60, fill="green", width=2,tag="ql")
        elif valores_qdy[v] >0:
            for i in range(qtd_vetores+1):
                canvas.create_polygon(x0+xi*a-5,yv+10,x0+xi*a, yv,x0+xi*a+5,yv+10, outline="green", width = 2, fill="white",tag="ql")
                canvas.create_line(x0+xi*a,yv, x0+xi*a, yv+60, fill="green", width=2,tag="ql")
                xi=xi+incremento
                    
            #Desenha a linha horizontal que liga todos os vetores de carga distribuida    
            canvas.create_line(x0+xa*a,yv+60, x0+(xi-incremento)*a, yv+60, fill="green", width=2,tag="ql")
      
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
    yb=hc-y0 #coordenada da parte de baixo da base
    yv=yb-22 #coordenada vertical da barra
    xv=x0-12 #coordenada do ponto de apoio esquerdo na linha da viga(origem)

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
    canvas.grid(column=6, row=0, padx=10, pady=10, rowspan=10,columnspan=4)
    
    #Inicializa e mostra os botoes que irao chamar as funções para exibir as cargas pontuais ou distribuida
    botao_qp = Button(frame_grafico, text="Cargas Pontuais", command=desenha_qp)
    botao_qd = Button(frame_grafico, text="Cargas Distribuidas", command=desenha_qd)
    botao_reacao = Button(frame_grafico, text="Reação", command=forca_reacao)
    botao_cortante = Button(frame_grafico, text="Diagrama Cortante", command=diagrama_cortante)
    botao_fletor = Button(frame_grafico, text="Momento Fletor", command=diagrama_momento_fletor)
    botao_normal = Button(frame_grafico, text="Diagrama Normal", command=diagrama_normal)
    frame_grafico.grid(row=0, column=6, sticky="news", padx=10, pady=10,rowspan=11)
    botao_qp.grid(column=7, row=10, padx=10, pady=10)
    botao_qd.grid(column=8, row=10, padx=10, pady=10)
    botao_reacao.grid(column=9, row=10, padx=10, pady=10)
    botao_sair.grid(column=9, row=11, padx=10, pady=10)
    botao_cortante.grid(column=6, row=11, padx=10, pady=10)
    botao_fletor.grid(column=7, row=11, padx=10, pady=10)
    botao_normal.grid(column=8, row=11, padx=10, pady=10)


    diagrama_cortante()
    diagrama_momento_fletor()
    diagrama_normal()
    forca_reacao()
    desenha_qd()
    desenha_qp()


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

    if len(qd) > 0:
        botao_insere_qd.grid_forget()
        qdfx_entry.config(state="disabled")
        qdfy_entry.config(state="disabled")
        qdxi_entry.config(state="disabled")
        qdxf_entry.config(state="disabled")

    elif (len(qd) == 0):
        botao_insere_qd.grid(column=5, row=3, padx=10, pady=10)
        qdfx_entry.config(state="normal")
        qdfy_entry.config(state="normal")
        qdxi_entry.config(state="normal")
        qdxf_entry.config(state="normal")

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
            
            if ((float(qpfy_entry.get()))==0) and ((float(qpfx_entry.get()))==0):
                messagebox.showerror(title="Info", message="Se a carga é igual a zero, então não há carga aplicada. Corrigir.")
                return False
            
            #só entra nesse for, a partir da segunda carga fornecida. Aí verifica se já tem uma carga pontual no mesmo ponto, fornecida anteriormente e calcula a resultante naquele ponto.
            #se a resultante for nula, remove a carga nula
            for i in range(2,len(qp),3):
                if (lista[i] == float(qpxi_entry.get())):
                    messagebox.showerror(title="Info", message="Já existe uma carga pontual no ponto fornecido.\nSerá calculado a resultante das forças nesse ponto e apenas um vetor resultante será indicado no diagrama.\nSe a resultante for nula, nada será exibido.")
                    lista[i-2]=lista[i-2]+round(float(qpfx_entry.get()),2)
                    lista[i-1]=lista[i-1]+round(float(qpfy_entry.get()),2)
                    if ((qp[i-2]==0) and (qp[i-1])==0):
                        qp.pop(i-2)
                        qp.pop(i-2)
                        qp.pop(i-2)
                        
                    listar_cargas()
                    return False

            #se for a primeira carga a ser fornecida, insere na lista de cargas
            lista.append(round(float(qpfx_entry.get()),2))
            lista.append(round(float(qpfy_entry.get()),2))
            lista.append(round(float(qpxi_entry.get()),2))

            listar_cargas()
            return False

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
            
            if float(qdxi_entry.get()) == float(qdxf_entry.get()):
                messagebox.showerror(title="Info", message="Se a carga distribuida está em um único ponto, então trata-se de uma carga pontual. Corrigir")
                return False
            
            if ((float(qdfy_entry.get()))==0) and ((float(qdfx_entry.get()))==0):
                messagebox.showerror(title="Info", message="Se a carga é igual a zero, então não há carga aplicada. Corrigir.")
                return False

            lista.append(round(float(qdfx_entry.get()),2))
            lista.append(round(float(qdfy_entry.get()),2))
            lista.append(round(float(qdxi_entry.get()),2))
            lista.append(round(float(qdxf_entry.get()),2))
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
            
            #verifica se a coordenada esquerda é a mesma que a direita.
            if float(coord_ex_entry.get()) == float(coord_dx_entry.get()) :
                messagebox.showerror(title="Info", message="A coordenada esquerda e a direita não podem ser iguais.")
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
hc=500

#margem esquerda e direita no grafico para inicio dos desenhos
x0=60
xf=440
#margem inferior no grafico para inicio dos desenhos
y0=60

#Menu
menubar = Menu(main)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Sobre", command=lambda: messagebox.showinfo(title="Info", message="Programa para cálculo do momento fletor, força cortante e normal em uma viga biapoiada.\n\
Desenvolvido em Python e interface gráfica feita com a biblioteca tkinter.\n\n\
Mecanica dos Solidos 1 - 2º Semestre de 2023\n\
Professor Honorato\n\n\
Aluno:\n\
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

qpfx_default = StringVar() #cargca pontual forca em x
qpfy_default = StringVar() #cargca pontual forca em y
qpxi_default = StringVar() #cargca pontual posicao x

qpfx_default.set("0.00")
qpfy_default.set("0.00")
qpxi_default.set("0.00")

qpfx_entry = Entry(frame_qp, width=10, textvariable=qpfx_default)
qpfy_entry = Entry(frame_qp, width=10, textvariable=qpfy_default)
qpxi_entry = Entry(frame_qp, width=10, textvariable=qpxi_default)

texto_qp=Label(frame_qp, text="Carga:")
texto_qp_fxi=Label(frame_qp, text="Fxi (N)")
texto_qp_fyi=Label(frame_qp, text="Fyi (N)")
texto_qp_xi=Label(frame_qp, text="Coordenada Xi (m)")

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

qdfx_default = StringVar() #carga distribuida forca em x
qdfy_default = StringVar() #carga distribuida forca em y
qdxi_default = StringVar() #carga distribuida inicio da força em x
qdxf_default = StringVar() #carga distribuida fim da força em x
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

carga_default = StringVar() #numero da carga a ser removida
carga_default.set("1")
carga_tipo_default = StringVar() #tipo de carga a ser removida
carga_tipo_default.set("Carga pontual")

carga_entry = Entry(frame_remover_cargas,width=10, textvariable=carga_default)
carga_entry.grid(row=4, column=1)

combobox = ttk.Combobox(frame_remover_cargas,state="readonly",values=["Carga pontual", "Carga Distribuida"], textvariable=carga_tipo_default)
combobox.grid(row=4,column=2, padx=10, pady=10)

botao_remover = Button(frame_remover_cargas, text="Remover", command=lambda: valida_entrada("remover",qd))
botao_remover.grid(column=5, row=4, padx=10, pady=10)

#Apoios
coord_ex_default = StringVar() #coordenada x do ponto de apoio esquerdo
coord_dx_default = StringVar() #coordenada x do ponto de apoio direit
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