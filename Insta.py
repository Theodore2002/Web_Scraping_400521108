import tkinter as tk
import urllib.error

import time
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.common.exceptions import TimeoutException
from urllib.request import urlopen
from PIL import Image, ImageTk

# user: dankabo12
# pass: @dankabo@


class LOGIN:
    def __init__(self, geo, title):
        self.root = tk.Tk()
        self.root.geometry(geo)
        self.root.title(title)
        self.root.configure(background="#EAEAEA")
        self.root.resizable(0, 0)
        self.i, self.j = 400, 200

        lab = tk.Label(self.root, text="Log in to your Instagram Account:", font="Aerial 12 bold", background="#EAEAEA")
        lab.place(x=22, y=5)

        user = tk.Label(self.root, text="Username:   @", font="Aerial 10", background="#EAEAEA")
        user.place(x=20, y=50)

        self.login = tk.Button(self.root, text="Sign in", font="Aerial 10", width=30, background="#EAEAEA", borderwidth=3, command=self.check_inputs)
        self.login.place(x=25, y=150)

        self.username = tk.Entry(self.root, width=25)
        self.username.place(x=116, y=53)

        pas = tk.Label(self.root, text="Password:", font="Aerial 10", background="#EAEAEA")
        pas.place(x=20, y=100)

        self.password = tk.Entry(self.root, width=25)
        self.password.place(x=116, y=103)

    def check_inputs(self):
        c1, c2 = True, True
        if self.username.get() == "":
            print("username can't be empty!")
            c1 = False
        if self.password.get() == "":
            print("password can't be empty!")
            c2 = False
        if c1 and c2:
            auto.user_pass(self.username.get(), self.password.get())
            self.open_panel()

    def open_panel(self):
        self.login['state'] = tk.DISABLED
        self.insta = GUI(f"700x450+{self.i}+{self.j}", self.username.get(), self)
        self.i += 15
        self.j += 15

        self.insta.account_box()
        self.insta.message_box()
        self.insta.download_story_box()


class GUI:
    def __init__(self, geo, title, other):
        self.title = title
        self.panel = tk.Toplevel(other.root)
        self.panel.geometry(geo)
        self.panel.title(title)
        self.panel.configure(background="#777777")
        self.panel.resizable(False, False)

    def account_box(self):
        auto.counts(self.title)  # returns a list so i can read post following followers counts, but xpath is not working
        acc_frame = tk.Canvas(self.panel, width=210, background="#EAEAEA")
        acc_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        acc_name = tk.Label(acc_frame, text=f"{self.title}", justify="center", font="Aerial 30", background="#EAEAEA")
        acc_name.pack(pady=10)

        img = tk.Label(acc_frame, image=auto.prof_img())
        img.pack(pady=10)

        acc_followers = tk.Label(acc_frame, text='followers', justify="center", font="Aerial 20 bold", background="#EAEAEA")
        acc_followers.pack(side=tk.BOTTOM, pady=7)

        acc_followings = tk.Label(acc_frame, text='followings', justify="center", font="Aerial 20 bold", background="#EAEAEA")
        acc_followings.pack(side=tk.BOTTOM, pady=7)

        acc_post = tk.Label(acc_frame, text='post count', justify="center", font="Aerial 20 bold", background="#EAEAEA")
        acc_post.pack(side=tk.BOTTOM, pady=7)

    def message_box(self):
        mes_frame = tk.Canvas(self.panel, width=210, background="#EAEAEA")
        mes_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        mes_direct = tk.Label(mes_frame, text="Send Direct Message to:", justify="center", font="Aerial 15")
        mes_direct.grid(row=0, column=0, columnspan=3)

        self.target_acc = tk.Entry(mes_frame, width=25)
        self.target_acc.grid(row=1, column=0, sticky='ne')

        mes_direct2 = tk.Label(mes_frame, text="@", justify="left", font="Aerial 12")
        mes_direct2.grid(row=1, column=0, sticky="nw")

        self.message = tk.Text(mes_frame, width=20, height=20, font="Aerial 10")
        self.message.grid(row=2, column=0, pady=10, rowspan=10, sticky="e", ipadx=15)

        send_message = tk.Button(mes_frame, text="Send Message!", command=auto.direct_mess)
        send_message.grid(row=12, column=0)

    def download_story_box(self):
        stor_frame = tk.Canvas(self.panel, width=200, background="#EAEAEA")
        stor_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        made_by = tk.Label(stor_frame, text="Armin Amirfatahi", font="Aerial 20", background="#EAEAEA")
        made_by.pack()

        s_id = tk.Label(stor_frame, text="400521108", font="Aerial 20", background="#EAEAEA")
        s_id.pack()

        stories = tk.Label(stor_frame, text="Download stories to:", font="Aerial 15", background="#EAEAEA")
        stories.pack(pady=15)

        self.stories_dir = tk.Text(stor_frame, width=20, height=10, font="Aerial 10")
        self.stories_dir.pack()

        download_stories = tk.Button(stor_frame, text="Download Stories", width=15, font="Aerial 15 bold", command=auto.download_story)
        download_stories.pack(pady=30)


class Automation:
    def __init__(self):
        serv = Service(executable_path='chromedriver.exe')
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=serv, options=chrome_options)

        self.driver.get("https://www.instagram.com/")

    def user_pass(self, user, pasw):
        user_inp = self.driver.find_element(value='//*[@id="loginForm"]/div/div[1]/div/label/input', by=By.XPATH)
        user_inp.send_keys(user)

        pass_inp = self.driver.find_element(value='//*[@id="loginForm"]/div/div[2]/div/label/input', by=By.XPATH)
        pass_inp.send_keys(pasw)

        log_but = self.driver.find_element(value='//*[@id="loginForm"]/div/div[3]/button', by=By.XPATH)
        log_but.click()

        not_now_btn1 = WebDriverWait(self.driver, 25).until(
            e_c.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
        not_now_btn1.click()

        not_now_btn2 = WebDriverWait(self.driver, 30).until(
            e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')))
        not_now_btn2.click()

    def counts(self, username):

        self.driver.get(f'https://www.instagram.com/{username}/')
        # posts = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.CSS_SELECTOR, '#mount_0_0_q4 > div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > ul > li:nth-child(1) > div > span')))
        # followings = self.driver.find_element(value='//*[@id="mount_0_0_RN"]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/li[2]/a/div/span', by=By.XPATH)
        # followers = self.driver.find_element(value='//*[@id="mount_0_0_RN"]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/li[3]/a/div/span', by=By.XPATH)
        # print([posts.text, followings.text, followers.text])
        # return [posts.text, followings.text, followers.text]

    def prof_img(self):
        try:
            img = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/div/div/span/img')))
            img = img.get_attribute("src")
        except TimeoutException:
            return None
        try:
            img = Image.open(urlopen(img))
        except urllib.error.URLError:
            return None
        img = img.resize((80, 80))
        img = ImageTk.PhotoImage(img)
        return img

    def direct_mess(self):
        reciever = insta1.insta.target_acc.get()
        message = insta1.insta.message.get("1.0", tk.END)
        self.driver.get('https://www.instagram.com/direct/inbox/')

        mes_but = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div[2]/div/div[3]/div/button')))
        mes_but.click()

        rec = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/input')))
        rec.send_keys(reciever)

        time.sleep(5)

        rec_but = WebDriverWait(self.driver, 30).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div[3]/button')))
        rec_but.click()

        next_but = WebDriverWait(self.driver, 10).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/button')))
        next_but.click()

        mes_area = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        mes_area.send_keys(message)

    def download_story(self):
        self.driver.get(f'https://www.instagram.com/{insta1.username.get()}/')
        directory = insta1.insta.stories_dir.get("1.0", tk.END)

        img_click = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/div/div/div/button')))
        img_click.click()

        pause_but = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/div/div[1]/section/div[1]/div/section/div/header/div[2]/div[2]/button[1]')))
        pause_but.click()

        i = 1
        while True:
            try:
                image = WebDriverWait(self.driver, 20).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/img')))
                img = image.get_attribute("srcset")
                with open(f"{directory}\{i}.png", 'wb') as f:
                    shutil.copyfileobj(img, f)
            except TimeoutException:
                break

            next_but = WebDriverWait(self.driver, 10).until(e_c.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/div[1]/div/section/div/button')))
            next_but.click()

            i += 1


if __name__ == "__main__":
    insta1 = LOGIN("300x200+50+50", "Login Page")
    auto = Automation()
    insta1.root.mainloop()