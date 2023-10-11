from tkinter import *
from pkg_resources import resource_filename


def cap_coord(x, y, button, pressed):
    
    if not pressed and button == mouse.Button.middle:
        texto_info["text"] = x, y
    elif not pressed and button == mouse.Button.right:
        return False  

def listen_mouse():
    def listen_mouse2():
        with mouse.Listener(on_click=cap_coord) as listener:
            listener.join() 
    threading.Thread(target=listen_mouse2).start()
    


#Funcao que checa a validade do valor fornecido pelo usuario
def callback(input): 
      
    if input.isdigit(): 
        return True
                             
    elif input == "":
        return True
  
    elif input == "-":
        return True

    elif input == ".":
        return True

    else: 
        texto_info["text"] = "Fornecer apenas número, sinal negaitivo ou separador decimal sendo o ponto."
        return False



main = Tk()

main.title("Mec Sol - Projeto Centroide")
resource1 = resource_filename(__name__, 'favicon.ico')
main.iconbitmap(resource1)

#Área do grafico
canvas = Canvas(main, width=700, height=550, bg="white")
canvas.create_line(0, 0, 700, 500, fill="red")
canvas.create_oval(100, 100, 120, 120, fill="red")

#Inicia as variaveis para os campos de entrada com o texto padrao
np1 = StringVar()
np2 = StringVar()
np3 = StringVar()
np4 = StringVar()
np1.set("1.00")
np2.set("2.00")
np3.set("3.00")
np4.set("4.00")
box1 = Entry(main, width=10, textvariable=np1)
box2 = Entry(main, width=10, textvariable=np2)
box3 = Entry(main, width=10, textvariable=np3)
box4 = Entry(main, width=10, textvariable=np4)

#Valida os valores fornecidos pelo usuario
reg = main.register(callback) 
box1.config(validate ="key", validatecommand =(reg, '%P'))
box2.config(validate ="key", validatecommand =(reg, '%P'))
box3.config(validate ="key", validatecommand =(reg, '%P'))
box4.config(validate ="key", validatecommand =(reg, '%P')) 

#atribui o valor fornecido pelo usuarios para as variasveis
valor_box1 = box1.get()
valor_box2 = box2.get()
valor_box3 = box3.get()
valor_box4 = box4.get()

#Inicia as variaveis de texto
info1=Label(main, text="Forneça apenas valores numéricos com separador decimal sendo o ponto")
texto_box1=Label(main, text="Valor 1:")
texto_box2=Label(main, text="Valor 2:")
texto_box3=Label(main, text="Valor 3:")
texto_box4=Label(main, text="Valor 4:")
texto_info = Label(main, text="", font="Arial")

#Após o usuario clicar no botao, chama a função que realiza os calculos
botao_1 = Button(main, text="Calcular", command=listen_mouse)

##Organizacao dos widget por grid
#informação de preenchimento ao usuario
info1.grid(column=0, row=0, padx=10, pady=10, columnspan=4)

#Textos informativos aos usuarios
texto_box1.grid(column=0, row=1, padx=10, pady=10)
texto_box2.grid(column=0, row=2, padx=10, pady=10)
texto_box3.grid(column=2, row=1, padx=10, pady=10)
texto_box4.grid(column=2, row=2, padx=10, pady=10)

#Box de entrada de dados
box1.grid(column=1, row=1, padx=10, pady=10)
box2.grid(column=1, row=2, padx=10, pady=10)
box3.grid(column=3, row=1, padx=10, pady=10)
box4.grid(column=3, row=2, padx=10, pady=10)

#Botao
botao_1.grid(column=3, row=4, padx=10, pady=10)

#Mostra os resultados dos calculos
texto_info.grid(column=0, row=5, padx=10, pady=10, columnspan=4)

#Tela de desenhos
canvas.grid(column=0, row=6, padx=10, pady=10, columnspan=4)


main.mainloop()