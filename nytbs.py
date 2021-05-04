import requests
import os
import urllib.request as req
import fpdf
from datetime import date
from bs4 import BeautifulSoup
import tkinter as tk

class GUI:
    def __init__(self, title):
        
        # Tkinter Window Initialization
        self.root = tk.Tk()
        self.root.geometry("300x180")
        self.frame = tk.Frame(self.root)
        self.root.title(title)

        # Value Options
        self.size = tk.StringVar(value="Letter")
        self.genre = tk.StringVar(value="Fiction")

        # Radio Buttons
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

def request_book_data(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    book_list = soup.find_all('li', {"class":"css-13y32ub"})
    return book_list

def parse_book_data(book_list, url):
    best_sellers = []

    for book in book_list:
        title = book.select('h3')[0].text.lower().title()
        author= book.select('p')[1].text
        
        # Index 2 returns how many weeks a book has been on the
        # best seller list, index 3 returns summary of the book; type <p>
        image_link = book.select('img')
        image_src = ""

        for pic in image_link:
            image_src = pic.get('src')
            url = req.urlretrieve(image_src, title+'.jpg')

        book_info = {
            "title": title,
            "author": author[3:], # skip 'by '
            "image" : image_src
        }

        best_sellers.append(book_info)
        
    return best_sellers

def write_PDF(best_sellers, head, size, filename):

    class PDF(fpdf.FPDF):
        def header(self):
            self.set_font('Arial', 'B', 25)
            self.cell(80)
            self.cell(30, 10,head, 0, 0, 'C')
            self.ln(20)

    pdf = PDF(format=size)
    pdf.add_page()

    count = 1

    for book in best_sellers:
        pdf.set_font("Arial", 'B', size=20)
        pdf.cell(100, 10, str(str(count) + ". " + book["title"]), 0, 1)
        pdf.set_font("Arial", size=15)
        pdf.cell(140, 10, "Author: " + book["author"], 0)

        # We shrink the contents of the PDF file depending on the desired paper size.
        # this allows for entries to not be split when there is more than one page.

        if size == "letter":
            pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=35)
        else:
            pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=30)
        pdf.ln()
        count += 1

    pdf.output(filename, 'F')

def start(genre, size):
    head = "The New York Times Bestsellers - " + genre.title()
    date_str = str(date.today().strftime("%m-%d-%y"))
    url = "https://nytimes.com/books/best-sellers/hardcover-" + genre

    filename = head + " " + date_str + " " + size + ".pdf"

    book_data = request_book_data(url)
    best_sellers = parse_book_data(book_data, url)

    write_PDF(best_sellers, head, size, filename) 

    for filename in os.listdir('.'):
        if filename.endswith('.jpg'):
            os.remove(filename)

def main():
    window = GUI("New York Times Bestsellers")

main()
