from tkinter import *
from pkg_resources import resource_filename
 

#Funcao que checa a validade do valor fornecido pelo usuario
def callback():

    canvas.grid_remove() 
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

        float(y1.get())
        float(y2.get())
        float(y3.get())
        float(y4.get())
        float(y5.get())

        float(ql.get())
        float(qlxi.get())
        float(qlxf.get())

        #Posicionamento da area do grafico
        canvas.grid(column=0, row=11, padx=10, pady=10, columnspan=6)
 
        info3["text"] = ""
    except:
        info3["text"] = "Apenas números, sinal negaitivo ou separador decimal."

main = Tk()
main.title("Mecanica dos solidos 1 - Diagrama de momentos")
#main.geometry("550x700")
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

yp1 = StringVar()
yp2 = StringVar()
yp3 = StringVar()
yp4 = StringVar()
yp5 = StringVar()
yp1.set("0.00")
yp2.set("0.00")
yp3.set("0.00")
yp4.set("0.00")
yp5.set("0.00")


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

y1 = Entry(main, width=10, textvariable=yp1)
y2 = Entry(main, width=10, textvariable=yp2)
y3 = Entry(main, width=10, textvariable=yp3)
y4 = Entry(main, width=10, textvariable=yp4)
y5 = Entry(main, width=10, textvariable=yp5)

ql = Entry(main, width=10, textvariable=qlp)
qlxi = Entry(main, width=10, textvariable=qlxip)
qlxf = Entry(main, width=10, textvariable=qlxfp)
dist = Entry(main, width=10, textvariable=qlxfp)

#atribui o valor fornecido pelo usuarios para as variaveis
valor_q1 = q1.get()
valor_q2 = q2.get()
valor_q3 = q3.get()
valor_q4 = q4.get()
valor_q5 = q5.get()

valor_x1 = x1.get()
valor_x2 = x2.get()
valor_x3 = x3.get()
valor_x4 = x4.get()
valor_x5 = x5.get()

valor_y1 = y1.get()
valor_y2 = y2.get()
valor_y3 = y3.get()
valor_y4 = y4.get()
valor_y5 = y5.get()

valor_qp = ql.get()
valor_qpxi = qlxi.get()
valor_qpxf = qlxf.get()
valor_dist = qlxf.get()

#Inicia as variaveis de texto
info1=Label(main, text="Forneça apenas valores numéricos com separador decimal sendo o ponto.")
info2 = Label(main, text="Distância entre os pontos de apoio em metros.")
info3 = Label(main, text="", font="Arial")
texto_1=Label(main, text="Carga 1:")
texto_2=Label(main, text="Carga 2:")
texto_3=Label(main, text="Carga 3:")
texto_4=Label(main, text="Carga 4:")
texto_5=Label(main, text="Carga 5:")
texto_qpkn=Label(main, text="Q (KN)")
texto_qlkn=Label(main, text="Q (KN/m):")
texto_x=Label(main, text="X (m)")
texto_y=Label(main, text="Y (m)")
texto_inicio=Label(main, text="Inicio (m):")
texto_fim=Label(main, text="Fim (m):")
texto_dist=Label(main, text="Distancia:")

texto_qp=Label(main, text="Cargas Pontuais")
texto_ql=Label(main, text="Carga Distribuida")

#Tela de desenhos
canvas = Canvas(main, width=450, height=400, bg="white")
canvas.create_line(0, 0, 700, 500, fill="red")
canvas.create_oval(100, 100, 120, 120, fill="red")



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
texto_y.grid(column=3, row=3, padx=10, pady=10)
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

y1.grid(column=3, row=4, padx=10)
y2.grid(column=3, row=5, padx=10, pady=10)
y3.grid(column=3, row=6, padx=10, pady=10)
y4.grid(column=3, row=7, padx=10, pady=10)
y5.grid(column=3, row=8, padx=10, pady=10)

ql.grid(column=5, row=4, padx=10)
qlxi.grid(column=5, row=5, padx=10, pady=10)
qlxf.grid(column=5, row=6, padx=10, pady=10)
dist.grid(column=1, row=10, padx=10, pady=10)


#Inicializacao e posicionamento do botao calcular
#Após o usuario clicar no botao, chama a função que realiza as checagens e essa, chama a funcao que realiza os calculos
botao_calcular = Button(main, text="Calcular", command=callback)
botao_calcular.grid(column=4, row=10, padx=10, pady=10)

#Mostra os resultados da conferencia dos dados de entrada
info2.grid(column=0, row=9, padx=10, pady=10, columnspan=6)
info3.grid(column=0, row=11, padx=10, pady=10, columnspan=6)

#Inicializacao e posicionamento do botao sair
botao_sair = Button(master=main, text="Sair", command=main.destroy)
botao_sair.grid(column=5, row=10)




main.mainloop()