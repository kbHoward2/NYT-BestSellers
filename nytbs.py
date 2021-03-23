import requests
import os
import urllib.request as req
import fpdf
from datetime import date
from bs4 import BeautifulSoup
import tkinter as tk

class GUI:

    def __init__(self, title):

        self.root = tk.Tk()
        self.root.geometry("300x180")
        self.frame = tk.Frame(self.root)
        self.root.title(title)

        self.size = tk.StringVar()
        self.genre = tk.StringVar()

        tk.Label(self.root, text="Document Size").grid(row=0, column=0, padx=30, pady=15)
        tk.Label(self.root, text="Genre").grid(row=0, column=1,padx=30, pady=15)

        tk.Radiobutton(self.root, text="Fiction", variable=self.genre, value="fiction").grid(row=1, column=0)
        tk.Radiobutton(self.root, text="Non\nFiction", variable=self.genre, value="nonfiction").grid(row=2, column=0)

        tk.Radiobutton(self.root, text="Letter", variable=self.size, value="letter").grid(row=1, column=1)
        tk.Radiobutton(self.root, text="Legal", variable=self.size, value="legal").grid(row=2, column=1)

        tk.Button(self.root, text="Start", command=self.start_button_cmd).grid(row=3, column=0, pady=15)
        tk.Button(self.root, text="Close", command=self.quit_button_cmd).grid(row=3, column=1, pady=15)
        
        self.root.mainloop()

    def quit_button_cmd(self):
        self.root.destroy()
        quit()
    
    def start_button_cmd(self):
       start(str(self.genre.get()), str(self.size.get()))

def start(genre, size):
    head = "The New York Times Bestsellers - " + genre.title()
    date_str = str(date.today().strftime("%m-%d-%y"))
    url = "https://nytimes.com/books/best-sellers/hardcover-" + genre

    filename = head + " " + date_str + " " + size + ".pdf"

    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    class PDF(fpdf.FPDF):
        def header(self):
            self.set_font('Arial', 'B', 25)
            self.cell(80)
            self.cell(30, 10,head, 0, 0, 'C')
            self.ln(20)

    book_list = soup.find_all('li', {"class":"css-13y32ub"})
    best_sellers = []

    # Find all the relevant information on the webpage
    for book in book_list:
        title = book.select('h3')[0].text.lower()
        title = title.title()
        author = book.select('p')[1].text
        # Index 2 returns how many weeks a book has been on the
        # best seller list, index 3 returns summary of the book; type <p>
        image_link = book.select('img')
        image_src = ""
        
        # We have to download each image, as the address provided by NYT isn't direct file path
        for pic in image_link:
            image_src = pic.get('src')
            url = req.urlretrieve(image_src, title+'.jpg')
        
        book_info = {
            "title": title,
            "author": author[3:], # skip 'by '
            "image" : image_src
        }

        best_sellers.append(book_info)

    # Begin with PDF creation after all the information has been stored in the dictonary
    pdf = PDF(format=size)
    pdf.add_page()

    # Print out relevant info for each book
    for book in best_sellers:
        pdf.set_font("Arial", 'B', size=20)
        pdf.cell(100,10, book["title"], 0, 1)
        pdf.set_font("Arial", size=15)
        pdf.cell(140,10, "Author: " + book["author"], 0)
        if size == "letter":
            pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=35)
        else:
            pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=30)
        pdf.ln()

    pdf.output(filename, 'F')

    for filename in os.listdir('.'):
        if filename.endswith('.jpg'):
            os.remove(filename)

def main():
    window = GUI("New York Times Bestsellers")

main()
