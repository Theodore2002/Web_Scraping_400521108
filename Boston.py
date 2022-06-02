import requests
from bs4 import BeautifulSoup
import tkinter as tk


class Connect:
    job_search = None
    job_name = None
    m, n = 800, 100

    def __init__(self):
        self.links = None
        self.jobs_dict = {}
        self.page = requests.get('https://boston.craigslist.org/search/jjj?')
        self.soup = BeautifulSoup(self.page.text, 'html.parser')

    def jobs_to_dict(self):
        jobs = self.soup.find_all(['select', 'options'])[-1]
        for i in jobs.find_all_next('option'):
            self.jobs_dict[i.text] = i.attrs['value']

    def show_results(self, job):
        job_h = self.jobs_dict[job]
        url = requests.get(f"https://boston.craigslist.org/search/{job_h}?")
        soup = BeautifulSoup(url.text, 'html.parser')
        job_list = soup.find_all(['h3'])
        jobs = [i.text for i in job_list]
        self.links = [i.a['href'] for i in job_list]
        return jobs

    def clicked_job(self, bind):
        try:
            selected = jobs_box.curselection()
            Connect.job_name = jobs_box.get(selected)
            selected = selected[0]
            link = self.links[selected]
            self.show_job_details(link)
        except IndexError:
            pass

    @staticmethod
    def show_job_details(link):
        a = requests.get(link)
        soup = BeautifulSoup(a.text, 'html.parser')

        des = soup.find_all(['section', 'div'])
        a = des[13].text
        start = a.index("compensation")
        end = a.index("Principals")
        de = a.index("QR Code Link to This Post")
        a = a[start:end]
        a = a.split("\n")
        a = [i for i in a if i]
        a.remove("QR Code Link to This Post")
        k = 1
        for i in range(len(a)):
            a.insert(k, "\n")
            k += 2
        Connect.top_level_window(Connect.job_name, a)

    @staticmethod
    def top_level_window(title, des):
        window = tk.Toplevel(root)
        window.geometry(f"700x350+{Connect.m}+{Connect.n}")
        Connect.m += 20
        Connect.n += 20
        window.title(title)
        window.resizable(False, False)
        description = tk.Text(window, width=700, height=350)
        description.pack(side=tk.LEFT, fill="y")
        for i in des:
            description.insert(tk.END, i)

    @classmethod
    def search(cls):
        cls.job_search = job_title.get()
        for i in c.show_results(cls.job_search):
            jobs_box.insert(tk.END, i)
        search_text.set("Searched!!!")
        clear_text.set("Click to clear")

    @staticmethod
    def clear():
        jobs_box.delete(0, jobs_box.size()-1)
        clear_text.set("Cleared!!!")
        search_text.set("Click to search")
        job_title.set("None")


c = Connect()
c.jobs_to_dict()


root = tk.Tk()
root.title("boston craigslist web application")
root.geometry("600x500+400+100")
root.configure(background="#EAEAEA")
root.resizable(False, False)

tk.Label(root, text="Choose a Job:", font="Aerial 20").place(x=0, y=10)

job_title = tk.StringVar(root, "None")
job_titles = tk.OptionMenu(root, job_title, *[i for i in c.jobs_dict])
job_titles.place(x=200, y=15)


search_text = tk.StringVar(root, "Click to search")
search_but = tk.Button(root, textvariable=search_text, font="Aerial 14", background="white", command=Connect.search)
search_but.place(x=20, y=60)

clear_text = tk.StringVar(root, "Click to clear")
clear_but = tk.Button(root, textvariable=clear_text, font="Aerial 14", background="white", command=Connect.clear)
clear_but.place(x=450, y=60)


frame = tk.Frame(root, background="#EAEAEA")
frame.place(x=18, y=110)

jobs_box = tk.Listbox(frame, background="white", height=24, width=74, font="Aerial 10 bold", justify=tk.LEFT)
jobs_box.pack(side='left', fill="y")

jobs_box.bind("<Double-Button>", c.clicked_job)

vbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=jobs_box.yview)
vbar.pack(side="right", fill="y")

jobs_box.config(yscrollcommand=vbar.set)



root.mainloop()
