import tkinter as tk
from tkinter import ttk
import customtkinter
import pickle
from PIL import Image, ImageTk
import cv2
import os
from carParkPicker import open_car_park_picker
from main import open_car_park_counter

#customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.a = True
        self._set_appearance_mode("System")

        self.title("Ventana principal")
        self.minsize(800,620)
        #self.geometry("800x620")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.large_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "carpark.jpg")),
                                                       size=(500, 150))
        self.large_image2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, "picker.png")),
                                                       size=(500, 350))
        self.large_image3 = customtkinter.CTkImage(Image.open(os.path.join(image_path, "carParkImg.png")),
                                                   size=(500, 350))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Navega ",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Car Park Picker",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Pick yourself",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Car Park Counter",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="",
                                                                   image=self.large_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.textbox = customtkinter.CTkLabel(self.home_frame, text="¿De que va el proyecto?", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.textbox.grid(row=1, column=0, padx=20, pady=(20, 0))

        self.textbox = customtkinter.CTkLabel(self.home_frame, text="¡Bienvenido al proyecto Car Park Counter!\n\n"
                                                                    "Este es un sistema inteligente de conteo de espacios de aparcamiento, \n"
                                                                    "diseñado para facilitar la tarea de encontrar un lugar para estacionar\n\n"
                                                                    "Nuestro proyecto utiliza cámaras para detectar automáticamente la cantidad de espacios disponibles\n"
                                                                    "en un estacionamiento y mostrar esta información en tiempo real en una pantalla\n\n"
                                                                    "El objetivo de este proyecto es reducir el tiempo que se pierde buscando estacionamiento\n"
                                                                    " y mejorar la experiencia general de los usuarios.\n\n"
                                                                    "¡Explora nuestras funciones y descubre cómo puedes mejorar tu próxima experiencia de estacionamiento\n con Car Park Counter!",
                                              font=customtkinter.CTkFont(size=14))
        self.textbox.grid(row=2, column=0, padx=20, pady=(20, 0))

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.textbox = customtkinter.CTkLabel(self.second_frame, text="Car Park Picker",
                                              font=customtkinter.CTkFont(size=24, weight="bold"))
        self.textbox.grid(row=1, column=0, padx=300, pady=(20, 0))

        self.textbox = customtkinter.CTkLabel(self.second_frame, text="Car Park Picker es un Seleccionador de espacios de Aparcamiento creado en OpenCV \n"
                                                                      " El programa necesita primero una foto tomada desde la parte superior de un estacionamiento\n"
                                                                      "para despues poder seleccionar manualmente los espacios validos en donde se puede estacionar un carro\n"
                                                                      "se seleccionan todos los espacios y se almacenan en un archivo binario para despues poder acceder a ellos.",
                                              font=customtkinter.CTkFont(size=18, weight="normal"))
        self.textbox.grid(row=2, column=0, padx=20, pady=(20, 0))

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                     image=self.large_image3)
        self.second_frame_large_image_label.grid(row=3, column=0, padx=20, pady=10)

        self.second_frame_button = customtkinter.CTkButton(self.second_frame, height=40, border_spacing=10,
                                                   text="antes y despues",
                                                   hover_color=("gray70", "gray30"), command=self.change_image)
        self.second_frame_button.grid(row=4, column=0)
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.textbox = customtkinter.CTkLabel(self.third_frame, text="Car Park Picker",
                                              font=customtkinter.CTkFont(size=24, weight="bold"))
        self.textbox.grid(row=1, column=0, padx=300, pady=(20, 0))
        self.third_frame_button = customtkinter.CTkButton(self.third_frame, height=40, border_spacing=10,
                                                           text="Pick yourself",
                                                           hover_color=("gray70", "gray30"), command=lambda : open_car_park_picker(self.third_frame))
        self.third_frame_button.grid(row=2, column=0, padx=20, pady=(20, 0))

        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.textbox = customtkinter.CTkLabel(self.fourth_frame, text="Car Park Counter (Video)",
                                              font=customtkinter.CTkFont(size=24, weight="bold"))
        self.textbox.grid(row=1, column=0, padx=100, pady=(20, 0))
        self.fourth_frame_button = customtkinter.CTkButton(self.fourth_frame, height=40, border_spacing=10,
                                                           text="Ver demostracion",
                                                           hover_color=("gray70", "gray30"),
                                                           command=lambda: open_car_park_counter())
        self.fourth_frame_button.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.description = customtkinter.CTkLabel(self.fourth_frame, text="Car park counter es un sistema que podria ayudar\n"
                                                                          "al usuario que busca un espacio disponible en algun estacionamiento\n"
                                                                          "ejemplo: un centro comercial, banco o establecimiento,\n"
                                                                          "tambien podria ayudar al gerente de alguno de estos negocios\n"
                                                                          "para poder tener una mejor administracion de sus estacionamientos\n"
                                                                          "asi como para obtener datos que despues puedan ser analizados\n"
                                                                          "y darles algun uso que contribuya ala organizacion.\n"
                                                                          "estos son solo algunos de los beneficios que tiene el sistema,\n\n"
                                                                          "LIMITACIONES Y POSIBLES MEJORAS A FUTURO:\n "
                                                                          "\nEl sistema no es perfecto y tiene sus limitaciones\n"
                                                                          "1) Puede confundir un objeto grande "
                                                                          "con un carro y por ende marcar el lugar como ocupado\n"
                                                                          "2) Actualmente los lugares de aparcamiento no cuentan con un identificador\n"
                                                                          "con el cual se pueda hacer referencia a ellos y ser mas especificos.\n"
                                                                          "3) Se puede agregar una función para identificar las secciones del\n"
                                                                          "estacionamiento y asignarles etiquetas como A, B, C, etc.\n"
                                                                          "Esto permitiría segmentar el estacionamiento en columnas, por ejemplo\n",
                                              font=customtkinter.CTkFont(size=16, weight="normal"))
        self.description.grid(row=3, column=0, padx=100, pady=(20, 0))
        self.text = customtkinter.CTkLabel(self.fourth_frame, text="REFERENCIA Y AGRADECIMIENTOS \n\n"
                                                                   "Quiero agradecer al creador del tutorial en YouTube del canal Murtaza's Workshop,\n"
                                                                   " por compartir su conocimiento y hacer posible que yo pueda desarrollar\n"
                                                                   " mi proyecto basado en su tutorial.\n"
                                                                   " tambien quiero agradecer a Dios por darme salud para seguir hasta acabar el proyecto\n"
                                                                   " a mi familia y a mi mismo por acompañarme \n"
                                                                   " y a mi cuerpo por permitirme hacer todo lo que hago gracias.",
                                              font=customtkinter.CTkFont(size=16, weight="normal"))
        self.text.grid(row=4, column=0, padx=100, pady=(20, 20))


        # select default frame
        self.select_frame_by_name("home")

        # Crear la ventana secundaria
        #secondary_window = tk.Toplevel(self)
        #secondary_window.title("Ventana Secundaria")

        #self.selector_button = customtkinter.CTkButton(master=self, text="Car Park Picker", command=lambda: open_car_park_picker(secondary_window))
        #self.selector_button.pack(padx=20, pady=20)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def change_image(self):
        self.a = not self.a
        if not self.a:
            self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                       image=self.large_image2)
            self.second_frame_large_image_label.grid(row=3, column=0, padx=20, pady=10)
        else:
            self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                         image=self.large_image3)
            self.second_frame_large_image_label.grid(row=3, column=0, padx=20, pady=10)


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

# Crear la ventana principal
#root = customtkinter.CTk()  # create CTk window like you do with the Tk window
#root.geometry("700x450")
# root = tk.Tk()
#root.title("Ventana Principal")

# Crear el botón para abrir la ventana del Car Park Selector con tkinter normal
#selector_button = ttk.Button(root, text="Car Park Picker", command=lambda: open_car_park_picker(secondary_window))
#selector_button.pack()

# Ejecutar el bucle principal de Tkinter
# root.mainloop()
if __name__ == "__main__":
    app = App()
    app.mainloop()