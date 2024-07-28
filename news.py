import requests
import io
import os
import webbrowser
from tkinter import *
from urllib.request import urlopen, Request
from PIL import Image, ImageTk


class NewsApp:
    def __init__(self):
        # fetch data
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?country=us&apiKey=e196a11127fe462297170e5f1c09dd43').json()
        # initial GUI load
        self.load_gui()
        # load the 1st news item
        self.load_news_item(0)

        # self.root.mainloop()

    def load_gui(self):
        self.root = Tk()
        self.root.title("Read News")
        # self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.config(background="black")

    def load_news_item(self, index):
        # clear the screen of the new news item
        self.clear()

        # image
        img_url = self.data['articles'][index]['urlToImage']
        if img_url is None:
            # Display "No Image" placeholder
            self.display_no_image()
        else:
            try:
                req = Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req) as response:
                    raw_data = response.read()
                im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
                photo = ImageTk.PhotoImage(im)
                label = Label(self.root, image=photo)
                label.image = photo  # Keep a reference to the image
                label.pack()
            except Exception as e:
                print(f"Error loading image: {e}")

        heading = Label(self.root, text=self.data['articles'][index]['title'], bg="black", fg="white", wraplength=350,
                        justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        details = Label(self.root, text=self.data['articles'][index]['description'], bg="black", fg="white",
                        wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))
        frame = Frame(self.root, bg="black")
        frame.pack(expand=True, fill=BOTH)

        if index != 0:
            prev = Button(frame, text="Prev", bg="white", fg="black", width=16, height=3,
                          command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text="Read More", bg="white", fg="black", width=16, height=3,
                      command=lambda: self.open_Link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != len(self.data['articles']) - 1:
            next = Button(frame, text="Next", bg="white", fg="black", width=16, height=3,
                          command=lambda: self.load_news_item(index + 1))
            next.pack(side=LEFT)

        self.root.mainloop()

    def display_no_image(self):
        image_path = os.path.join('assets', 'imgNotFound.jpg')
        img = Image.open(image_path)
        resized = img.resize((350, 250))
        photo = ImageTk.PhotoImage(resized)
        img_label = Label(self.root, image=photo)
        img_label.image = photo
        img_label.pack()

    def open_Link(self, url):
        webbrowser.open(url)

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()


obj = NewsApp()
