import importlib
import subprocess
import tkinter as tk
from tkinter.constants import *
import sys
from os.path import join, dirname
import logging
import base64

logging.basicConfig(level=logging.INFO)

ANDON_SITE = "http://fc-andons-na.corp.amazon.com/HDC3?category=Pick&type=No+Scannable+Barcode"
LOGIN_URL = "https://fcmenu-iad-regionalized.corp.amazon.com/login"

#code has launcher but needs a function that user can add website and html element that needs to be seen for program to screenshot it
websites = {
    'https://www.psu.edu': '/html/body/div/section[5]/div/div',
    'https://www.reddit.com': "/html/body/shreddit-app/div/div[1]/div[2]/main/dsa-transparency-modal-provider/shreddit-feed/article[1]",
    'https://www.kaggle.com':'/html/body/main/div[1]/div/div[5]/div[2]/div/div/section[3]/div[2]/div[3]'
    #'https://fcmenu.iad.regionalized.corp.amazon.com/HDC3/entry/200'
}

class reporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Andon Resolver")
        self.root.geometry("300x200")
        self.root.resizable(width=False, height=False)
        self.root.configure(background="white")
        self.badge = tk.IntVar()
        self.newWindow = tk.BooleanVar()
        self.headless = tk.BooleanVar()
        self.output_text = tk.StringVar()
        self.output_text.set(value="")
        
        try:
            icon_path = 'Resources/Problem.ico'
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            None
        self.create_widgets(self.badge, self.newWindow, self.headless, self.output_text)

    def create_widgets(self, badge, nwWindow, bool_head, output_text):
        label = tk.Label(self.root, text="Badge Number", font=("Arial", 10), fg="#333333", justify="center", background="white")
        label.place(x=10, y=80, width=100, height=30)

        entry_Badge = tk.Entry(self.root, borderwidth="2px", font=("Arial", 10), fg="#333333", justify="center", textvariable=badge)
        entry_Badge.delete(first=0)
        entry_Badge.place(x=115, y=80, width=100, height=30)
        entry_Badge.focus()

        # Checkbutton
        check_button = tk.Checkbutton(self.root, text="Hide Browser Window?", font=("Arial", 10), fg="#333333", variable=bool_head, anchor='w', background="white")
        check_button.place(x=10, y=20, width=160, height=25)

        newWindow_chkButton = tk.Checkbutton(self.root, text='New Window?', font=('Arial', 10), fg='#333333', variable=nwWindow, anchor='w', background='white')
        newWindow_chkButton.place(x=10, y=50, width=130, height=25)
        # Button
        button = tk.Button(self.root, text="Resolve Andons", bg="#4CAF50", font=("Arial", 10, "bold"), fg="white", command=self.gather)
        button.place(x=90, y=135, width=120, height=30)
        
        # Label
        output = tk.Label(self.root, textvariable=output_text, font=("Arial", 10), fg="#333333", justify="center", background="white", anchor='w')
        output.place(x=60, y=170, width=300, height=20)

    def gather(self):
        from selenium.common.exceptions import NoSuchElementException
        try:
            badge_value = str(self.badge.get())
            boolean = self.headless.get()
            if badge_value:
                self.root.update()
                self.main(boolean)
            else:
                self.output_text.set("Enter Valid Badge/Count entry")
                self.root.update()
        except tk.TclError:
            self.output_text.set("Enter Valid Badge/Count entry")
            self.root.update()
        except NoSuchElementException as e:
            print(e)
        except Exception as e:
            print(e)
    
    def install_module(self, module_name):
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            logging.info(f"{module_name} not found. Installing it now...")
            try:
                subprocess.run([sys.executable, '-m', 'pip',
                            'install', module_name], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error installing {module_name}: {e}")
                sys.exit(1)

    def navigate_to_website(self, driver, url, max_attempts=5):
        from selenium.common.exceptions import WebDriverException
        exception_count = 0
        while exception_count < max_attempts:
            try:
                driver.get(url)
                return
            except WebDriverException as se:
                exception_count += 1
                if "ERR_NAME_NOT_RESOLVED" in se.msg:
                    logging.error(f'WebDriverException #{exception_count}:\n Error in loading URL:: {se.msg}\n')
                else:
                    logging.error(f'WebDriverException #{exception_count}:\n Error in loading URL:: {se.msg}\n')
    def main(self, head):
        self.install_module('selenium')
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.common.exceptions import NoSuchElementException
        from selenium.webdriver.common.action_chains import ActionChains
        import io
        from PIL import Image

        optionals = ChromeOptions()
        optionals.add_argument('--log-level=3')
        optionals.add_argument('--force-device-scale-factor=0.7')
        optionals.add_argument('--disable-blink-features=AutomationControlled')
        optionals.add_argument('--disable-notifications')

        if head:
            optionals.add_argument('--headless')

        driver = webdriver.Chrome(options=optionals)
        driver.implicitly_wait(5)
        pngCount = 0
        offset = 200
        actions = ActionChains(driver)
        

        for site, xpath in websites.items():
            driver.maximize_window()
            self.navigate_to_website(driver, site)
            try:
                actions.move_to_element(driver.find_element('xpath',xpath)).perform()
                # actions.scroll_by_amount(0,offset).perform()
                # driver.execute_script(f'window.scrollBy(0,{offset});')
                image_binary  = driver.find_element('xpath', xpath).screenshot_as_png
                img = Image.open(io.BytesIO(image_binary))
                pngCount += 1
                img.save(f"image{pngCount}.png")
            except NoSuchElementException as e:
                logging.error(f"Element not found for site '{site}' with XPath '{xpath}': {e}")

        driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = reporterApp(root)
    root.mainloop()