import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
# PIL: directly read files from url, and won't download them separately
from PIL import Image, ImageTk
from io import BytesIO  # read byte type image


class ImageBing:
    text = None
    images = []
    true_images = []

    def __init__(self, word):
        self.word = word
        self.url = f"https://www.bing.com/images/search?q={word}&form=HDRSC2&first=1&tsc=ImageHoverTitle"
        page = page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all(['a', 'img'])
        key_word = "amp;"  # after &
        im_list = []
        for i in images:
            try:
                im_list.append(i.img['src2'])
            except (KeyError, TypeError, AttributeError):
                pass
        for i in im_list:
            # print(i)
            a = i.split("&")
            true_link = ""
            for k in a:
                true_link += k
                true_link += "&amp;"
            link = true_link[:-5]
            # print(link)
            ImageBing.true_images.append(link)

    @classmethod
    def search(cls):
        cls(topic.get())
        clear_text.set("Click to clear")
        cls.text = ScrolledText(root, wrap=tk.WORD, width=100)
        cls.text.place(x=20, y=100)
        search_text.set("Searching...")
        j = 0
        for i in cls.true_images:
            img = Image.open(BytesIO(requests.get(i).content))
            img = img.resize((145, 100))
            # **************************************** in case images didn't show up, add img.show() to next line
            img = ImageTk.PhotoImage(img)
            cls.text.image_create(tk.INSERT, image=img)
            j += 1
            if j == 15:
                break
        search_text.set("Searched!")

    @classmethod
    def clear(cls):
        cls.text.destroy()
        search_text.set("Click to search")
        clear_text.set("Cleared!")


root = tk.Tk()
root.title("Bing images")
root.geometry("600x500+400+100")
root.configure(background="#EAEAEA")
root.resizable(False, False)

tk.Label(root, text="Choose a topic:", font="Aerial 20").place(x=0, y=10)

topic = tk.Entry(width=60)
topic.place(x=220, y=22)


search_text = tk.StringVar(root, "Click to search")
search_but = tk.Button(root, textvariable=search_text, font="Aerial 14", background="white", command=ImageBing.search)
search_but.place(x=20, y=60)

clear_text = tk.StringVar(root, "Click to clear")
clear_but = tk.Button(root, textvariable=clear_text, font="Aerial 14", background="white", command=ImageBing.clear)
clear_but.place(x=450, y=60)


root.mainloop()
