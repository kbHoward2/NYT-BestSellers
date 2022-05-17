# NYT-BestSellers

![Alt text](nytbs2.png?raw=true "PDF")

## About
A script to pull the New York Times BestSellers into a PDF file.

## Features
* Export to PDF or CSV for easy printing or spreadsheet view.
* Configurable options including summaries, book cover, author.
* Letter or Legal size.

### Operating System Dependencies
* python3.7+
* python venv
* pip3
* git (optional)

### Python Dependencies
* Tkinter
* FPDF
* BeautifulSoup4
* Requests

## Setup Virtual Environment 
### Ubuntu 
1. Download the zip file or clone the repository with git.
2. `git clone https://github.com/kbHoward2/NYT-BestSellers.git`
3. `python3 -m venv /path/to/repository`
4. `cd NYT-BestSellers`
5. `apt install python3-tk` 
6. pip install -r requirements.txt
7. python3 main.py

### Windows
See the releases page for bundle Windows EXE for your machine.

## Usage
Simply select your options and click start a PDF document will be output in the directory of the binary executable.

## Future Plans 
- [x] Export checkbox for .csv and .txt files.
- [x] Option for Book Summary.
- [x] Option for Text Only.
- [x] Option for Image Only.
- [ ] Headless execution through commandline. 
