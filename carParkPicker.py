import cv2
# Importamos la biblioteca "pickle" para serializar objetos y guardarlos en archivos
import pickle
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def open_car_park_picker(window):
    def update_image(label, img):
        """ Actualiza la imagen en un Label de Tkinter con una imagen de PIL convertida a PhotoImage"""
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.config(image=imgtk)

    width, height = 107, 48

    try:
        with open('CarParkPos', "rb") as f:
            posList = pickle.load(f)
    except:
        posList = []

    def mouseClick(events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            posList.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList.pop(i)
        # Abrimos un archivo llamado 'CarParkPos' en modo de escritura binaria ('wb') utilizando un contexto 'with'
        # La variable 'f' representa el archivo abierto
        # Llamamos a la función 'pickle.dump()' para serializar el objeto 'posList' y guardarlo en el archivo 'f'
        with open('CarParkPos', "wb") as f:
            pickle.dump(posList, f)

    # Create a Tkinter window
    #window = tk.Tk()
    #window.title("CAR PARK PICKER")

    #style = ttk.Style()
    #style.configure("TLabel", font=("Arial", 18))
    # Crear un Label para mostrar la imagen
    label = tk.Label(window)
    label.grid(row=3, column=0, padx=20, pady=(20, 0))

    while True:
        img = cv2.imread("carParkImg.png")

        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        # Actualizar la imagen en el Label
        update_image(label, img)
        # Esperar unos milisegundos
        # window.after(1)

        cv2.waitKey(1)
        window.update()

#root = tk.Tk()
#root.title("CAR PARK PICKER")
#open_car_park_picker(root)