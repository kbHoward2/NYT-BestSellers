import requests
import os
import urllib.request as req
import fpdf
import csv
from datetime import date
from bs4 import BeautifulSoup
import tkinter as tk

class GUI:

    def __init__(self, title):
        # Tkinter Window Initialization
        self.root = tk.Tk()
        self.root.geometry("300x400")
        self.frame = tk.Frame(self.root)
        self.root.title(title)
        self.root.resizable(False, False)

        # Value Options
        self.size = tk.StringVar(value="Letter")
        self.genre = tk.StringVar(value="Fiction")
        self.summary = tk.IntVar(value = 0)
        self.images = tk.IntVar(value = 1)
        self.weeks_as_bs = tk.IntVar(value = 0)
        self.export_csv = tk.IntVar(value = 0)


        # Label Frames
        lf_genre = tk.LabelFrame(self.root, text="Genre")
        lf_genre.pack(ipadx=20,padx=15, pady=5)

        lf_size = tk.LabelFrame(self.root, text="Document Size")
        lf_size.pack(padx=15, pady=5)

        lf_options = tk.LabelFrame(self.root, text="Optional")
        lf_options.pack(padx=15, pady=5)

        # Radiobuttons
        tk.Radiobutton(lf_genre, text="Fiction", variable=self.genre, value="fiction").pack(anchor="w")
        tk.Radiobutton(lf_genre, text="Non\nFiction", variable=self.genre, value="nonfiction").pack(anchor="w")

        tk.Radiobutton(lf_size, text="Letter", variable=self.size, value="letter").pack(anchor="w")
        tk.Radiobutton(lf_size, text="Legal", variable=self.size, value="legal").pack(anchor="w")

        # Checkbuttons 
        tk.Checkbutton(lf_options, text="Book Images", variable=self.images, onvalue=1, offvalue=0).pack(anchor="w")
        tk.Checkbutton(lf_options, text="Include Summary", variable=self.summary, onvalue=1, offvalue=0).pack(anchor="w")
        tk.Checkbutton(lf_options, text="Include Weeks on List", variable=self.weeks_as_bs, onvalue=1, offvalue=0).pack(anchor="w")
        tk.Checkbutton(lf_options, text="Export CSV", variable=self.export_csv, onvalue=1, offvalue=0).pack(anchor="w")

        # Command Buttons
        tk.Button(self.root, text="Start", command=self.start_button_cmd).pack(side="left", padx="25")
        tk.Button(self.root, text="Close", command=self.quit_button_cmd).pack(side="right", padx="25")

        self.root.mainloop()

    def quit_button_cmd(self):
        self.root.destroy()
        quit()
    
    def start_button_cmd(self):
       options = [str(self.genre.get()), self.size.get(), self.summary.get(), 
       self.images.get(), self.weeks_as_bs.get(), self.export_csv.get()]
       start(options)

def request_book_data(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    book_list = soup.find_all('li', {"class":"css-13y32ub"})
    return book_list

def parse_book_data(book_list, url, options):
    best_sellers = []
    
    for book in book_list:
        title = book.select('h3')[0].text.lower().title()
        author= book.select('p')[1].text
        img_src = None
        summary = None
        weeks_as_bs = None

        # Index 2 returns how many weeks a book has been on the
        # best seller list, index 3 returns summary of the book; type <p>
        if( options[2] == 1):
            summary = book.select('p')[3].text
            summary = summary.encode('utf-8')

        if(options[3] == 1):
            image_link = book.select('img')
            image_src = ""
            for pic in image_link:
               image_src = pic.get('src')
               url = req.urlretrieve(image_src, title+'.jpg')
        else:
            image_src = None
       
        if (options[4] == 1):
            weeks_as_bs = book.select('p')[0].text

        book_info = {
            "title": title,
            "author": author[3:], # skip 'by '
            "image" : image_src,
            "summary" : summary,
            "weeks_as_bs" : weeks_as_bs
        }
        # print(str(summary.decode('utf-8')))
        best_sellers.append(book_info)
        
    return best_sellers

def write_PDF(best_sellers, head, size, filename):

    filename = filename + ".pdf"

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
        pdf.cell(140, 10, "Author: " + book["author"], 0, 1)

        if (book["weeks_as_bs"] != None):
            pdf.cell(70, 10, book["weeks_as_bs"], 0, 1)

        # We shrink the contents of the PDF file depending on the desired paper size.
        # this allows for entries to not be split when there is more than one page.
        if (book["summary"] != None):
            pdf.set_font("Arial", 'I', size=12)
            pdf.multi_cell(100, 5, str(book["summary"].decode('latin-1')), 0, 'L', False)
        else:
            pass

        if (book["image"] != None):
            if size == "letter":
                pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=45)
            else:
                pdf.image(name=str(book["title"] + ".jpg"), x=150, w=25,h=40)

        pdf.ln()
        count += 1

    pdf.output(filename, 'F').encode('latin-1')

def start(options):
    head = "The New York Times Bestsellers - " + options[0].title()
    date_str = str(date.today().strftime("%m-%d-%y"))
    url = "https://nytimes.com/books/best-sellers/hardcover-" + options[0] 

    filename = head + " " + date_str + " " + options[1]

    book_data = request_book_data(url)
    best_sellers = parse_book_data(book_data, url, options)

    write_PDF(best_sellers, head, options[1], filename) 

    if (options[5]):
        create_csv(options, best_sellers, filename)

    for filename in os.listdir('.'):
        if filename.endswith('.jpg'):
            os.remove(filename)

def create_csv(options, best_sellers, filename):
    with open (filename + ".csv", mode="w", newline='') as csv_file:
        fieldnames = ['Title', 'Author', 'Summary', 'Weeks', 'Image']  
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
        writer.writeheader()
        for book in best_sellers:
            writer.writerow({'Title': book["title"], 'Author': book["author"],
            'Summary': book["summary"], 'Weeks': book["weeks_as_bs"], 'Image': book["image"]})

def main():
    window = GUI("New York Times Bestsellers")

main()
