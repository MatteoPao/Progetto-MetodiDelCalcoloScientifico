import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

from imageProcessing import compress_matrix

#Queste righe generano la finestra che conterrà l'interfaccia
root = Tk()
root.title("Simple BMP Compresser")
root.geometry('480x300')

startingImage = None
imgArr = None

'''
OPEN_FILE
Quesa funzione viene chiamata alla pressione del bottone Import file
'''
def openFile():
    global startingImage
    global my_img
    global imgArr

    #Apro la finestra del filesystem per la selezione di un file bmp
    filepath = filedialog.askopenfilename(
        initialdir = "\\TestImage", 
        filetypes = (("Bitmap File","*.bmp"),))

    #Salvo l'immagine e la converto in array
    startingImage = Image.open(filepath)
    imgArr = (np.array(startingImage))

    #Imposto l'immagine importata come thumbnail
    thumb = startingImage.copy()
    thumb.thumbnail((150, 150))
    my_img = ImageTk.PhotoImage(thumb)
    thumbnail_image.itemconfig(image_on_canvas, image = my_img)

    filename = filepath.split("/")[-1]
    imageNameLabel['text'] = "Input Image: " + filename + " " + str(imgArr.shape)
    
    entry1.config(state='normal')
    info_label1.config(text = '(1, ' + str(min(imgArr.shape)) +')')
    #chiamo enableStart per verificare se sussistono le condizioni per la compressione
    enableStart()

'''
EDIT_IMAGE
'''
def editImage():
    #leggo i valori F e d
    f = int(var1.get())
    d = int(var2.get())

    #Comprimo, modifico e decomprimo l'immagine
    resArr = compress_matrix(imgArr.copy(), f, d)
    resImage = Image.fromarray(resArr)

    #Mostro i risultati
    startingImage.show()
    resImage.show()

'''
ENABLE_START
Verifica che le condizioni necessarie per effettuare la conversione siano rispettate
'''
def enableStart(*args):
    x = var1.get()
    y = var2.get()

    if x.isdigit() and x != '0' and int(x) <= min(imgArr.shape):
        entry2.config(state='normal')
        info_label2.config(text = '(0, ' +  str(2*int(x)- 2) +')')
        if y.isdigit() and y != '0\\d' and int(y) <= (2*int(x)-2):
            startButton.config(state='normal')
            return
        else:
            var2.set(str(y[:-1]))
            if y[:-1] == '':
                startButton.config(state='disabled')
    else:
        var1.set(x[:-1])
        if x[:-1] == '':
            entry2.config(state='disabled')

#Questa sezione crea gli oggetti del menu sinistro
menu_left = Frame(root, width=150)
menu_left_upper = Frame(menu_left, width=200, height=10)
menu_left_middle = Frame(menu_left, width=200)
menu_left_lower = Frame(menu_left, width=200)

space_up = Frame(menu_left, height=23)
inputButton = Button(menu_left_upper, text = 'Import File', padx = 35, pady = 10, bd = 5, command = openFile)

var1 = StringVar(root)
var2 = StringVar(root)
var1.trace("w", enableStart)
var2.trace("w", enableStart)

label1 = Label(menu_left_middle, text = 'F', padx = 20)
label2 = Label(menu_left_lower, text = 'd', padx = 19)
info_label1 = Label(menu_left_middle, text = '')
info_label2 = Label(menu_left_lower, text = '')
entry1 = Entry(menu_left_middle, width = 15, borderwidth = 1, textvariable=var1, state = DISABLED)
entry2 = Entry(menu_left_lower, width = 15, borderwidth = 1, textvariable=var2, state = DISABLED)


#Questa sezione posiziona gli oggetti del menu sinistro
space_up.pack()
inputButton.pack()

info_label1.grid(row = 0, column = 0, columnspan = 2)
info_label2.grid(row = 0, column = 0, columnspan = 2)
label1.grid(row=1, column=0)
label2.grid(row=1, column=0)
entry1.grid(row=1, column=1)
entry2.grid(row=1, column=1)

menu_left_upper.pack(side="top", fill="both", expand=True)
menu_left_middle.pack(side="top", fill="both", expand=True)
menu_left_lower.pack(side="top", fill="both", expand=True)

#Questa sezione crea e posizoina gli oggetti della zona destra
title_frame = Frame(root)

imageNameLabel = Label(title_frame, text = "Input Image: ", pady = 25)
imageNameLabel.pack()

thumbnail_area = Frame(root, width=300, height=300)
thumbnail_area.grid(row=1, column=1)
my_img = ImageTk.PhotoImage(Image.open("Thumbnail.gif"))
thumbnail_image = Canvas(thumbnail_area, width=150, height=150)
thumbnail_image.pack()
image_on_canvas = thumbnail_image.create_image(0, 0, anchor = NW, image = my_img)

#Questa sezione crea e posiziona il bottone START
status_frame = Frame(root)
startButton = Button(status_frame, 
    text = 'Start Compression',
    pady = 20, bd = 5,
    state = DISABLED,
    command = editImage)
startButton.pack(fill="both", expand=True)

#Questa sezione compone la GUI finale
menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
title_frame.grid(row=0, column=1, sticky="ew")
thumbnail_area.grid(row=1, column=1, sticky="nsew") 
status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()