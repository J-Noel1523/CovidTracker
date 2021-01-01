import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import ImageTk, Image

# pass in original and user requested url's
def data_from_html_url(url):
    data = requests.get(url)
    return data

def covid_data(url="https://www.worldometers.info/coronavirus"):
    html_data = data_from_html_url(url)
    bs = BeautifulSoup(html_data.text, "html.parser")
    html_info = bs.find("div", {'class': 'content-inner'}).find_all("div", {'id': 'maincounter-wrap'})
    all_data = ""
    # try catch block for solving U.S. search problem (list index out of bounds)
    try:
        for indexed in html_info:
            text = indexed.select("h1", {'class': 'None'})[0].get_text()
            count = indexed.select("span", {'class': 'None'})[0].get_text()
            all_data = all_data +' ' + text + ' ' + count + '\n'
    except:
        print('waiting...')
    return all_data

def get_country():
    name = textfield.get()
    # f string to pass as user's url request
    url = f"https://www.worldometers.info/coronavirus/country/{name}"
    main_label['text'] = covid_data(url)

def reload():
    new_data = covid_data()
    main_label['text'] = new_data

covid_data()
# initiate tkinter window; set height and width; set font; set title; resize image; etc
root = Tk()
root.geometry("1000x1000")
root.title("COVID-19 Tracker")
fonts = ("poppins", 25, "bold")
banner = Image.open("Coronavirus-CDC-645x645.png")
banner = banner.resize((250, 250), Image.ANTIALIAS)
tkImage = ImageTk.PhotoImage(banner)
image_display = Label(root, image=tkImage).pack()


# main covid information (cases, deats, etc)
main_label = Label(root, text=covid_data(), font=fonts)
main_label.pack()

textfield = Entry(root, width=50)
textfield.pack()

empty_space = Label(root, text="")
empty_space.pack()

get_btn = Button(root, text="Get Data", font=fonts, relief='solid', command=get_country)
get_btn.pack()

empty_space = Label(root, text="")
empty_space.pack()

btn = Button(root, text='Reload data', font=fonts, relief='solid', command=reload)
btn.pack()

empty_space = Label(root, text="Source: worldometers")
empty_space.pack()

root.mainloop()