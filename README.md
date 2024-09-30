# Estatus
Realizar un programa que sea capaz de revisar el estado de tu aplicación.

# THREADING
Se trata de una libreria que nos permite crear y manipular hilos, es este caso son especialmente utiles en modo demonio ya que son especialmente utiles para operaciones de monitorización de servicios o aplicaciones.

En este caso tenemos un programa principal que muestra 2 imagenes de una API de imagenes utilizando asincronia y tkinter.

# APLICACIÓN
Creamos un hilo que se encargue de mostrar la interfaz con las imagenes que obtuvimos de la API (Este hilo sera nuestra aplicación o servicio)

>Función `interface()`
```
def interface(images: list) -> None:
    root = tk.Tk()
    root.title("Demonios")
    for i, img in enumerate(images):
        img_tk = ImageTk.PhotoImage(img)
        lb = tk.Label(root, image=img_tk)
        lb.image = img_tk
        lb.grid(row=i, column=0)

    bt_exit = tk.Button(root, text="Exit", command=root.destroy)
    bt_exit.grid(row=0, column=1)
    
    root.mainloop()
```

>Hilo encargado de correr función interface
```
hilo_show_interface = threading.Thread(target=interface, args=(images,))
hilo_show_interface.start()
```

Creamos un hiloo que se encargue de revisar el estado del hilo de la aplicación o servicio, es decir de la interfaz que muestra las imagenes

>Función `revisar_estado_aplicacion()` 
```
def revisar_estado_aplicacion(hilo_show_interface: threading.Thread) -> None:
    while True:
        # Imprimir animación de revisión de estado
        animation2 = ["-    ", " -   ", "  -  ", "   > "]
        for i in range(4):
            time.sleep(0.1)
            sys.stdout.write("\r" + "Alive " + animation2[i % len(animation2)] + str(hilo_show_interface.is_alive()))
            sys.stdout.flush()
```

>Hilo de monitoreo de aplicación o servicio
```
hilo_revisar_estado = threading.Thread(target=revisar_estado_aplicacion, daemon=True, args=(hilo_show_interface,))
hilo_revisar_estado.start()
```

# EJECUCIÓN
Observaremos que en todo momento en la terminal observaremos el estado de nuestra aplicación
<img src="https://raw.githubusercontent.com/jhotwox/Estatus/refs/heads/main/2024-09-29_200703.png">

Observaremos que si cerramos la aplicación, el estado cambia a False
<img src="https://raw.githubusercontent.com/jhotwox/Estatus/refs/heads/main/2024-09-29_200730.png">
