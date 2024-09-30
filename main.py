import threading
import time
import sys
import tkinter as tk
import asyncio
import aiohttp
from PIL import Image, ImageTk
from io import BytesIO

image_URLS = [
    "https://picsum.photos/200/200",
    "https://picsum.photos/200/200",
]

async def fetch_image(session: aiohttp.ClientSession, url: str) -> Image:
    async with session.get(url) as response:
        if response.status == 200:
            img_data = await response.read()
            return Image.open(BytesIO(img_data))
        return None

async def fetch_all_images() -> list:
    async with aiohttp.ClientSession() as session:
        coroutines = [fetch_image(session, url) for url in image_URLS]
        images = await asyncio.gather(*coroutines)
        return images

def revisar_estado_aplicacion(hilo_show_interface: threading.Thread) -> None:
    while True:
        # Imprimir animación de revisión de estado
        animation2 = ["-    ", " -   ", "  -  ", "   > "]
        for i in range(4):
            time.sleep(0.1)
            sys.stdout.write("\r" + "Alive " + animation2[i % len(animation2)] + str(hilo_show_interface.is_alive()))
            sys.stdout.flush()

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

def main():
    images = asyncio.run(fetch_all_images())
    # Crear un hilo para revisar el estado de la aplicación, iniciarlo como un hilo demonio
    hilo_show_interface = threading.Thread(target=interface, args=(images,))
    hilo_show_interface.start()
    
    hilo_revisar_estado = threading.Thread(target=revisar_estado_aplicacion, daemon=True, args=(hilo_show_interface,))
    hilo_revisar_estado.start()

    while True:
        input("")

if __name__ == "__main__":
    main()