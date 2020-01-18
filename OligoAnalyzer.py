from time import sleep

import webbrowser

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from jinja2 import Template
from pathlib import Path
from configparser import ConfigParser

user = ""
pw = ""
ini = Path("user.ini")
if ini.exists():
    config = ConfigParser()
    config.read(ini)
    try:
        user = config.get("main", "user")
        pw =  config.get("main", "pw")
    except:
        pass
if not user.strip():
    user = input("Username: ")
else:
    print("User name: " + user)
if not pw.strip():
    pw = input("Password: ")


print("Zkopirujte z Excelu dva sloupce jmeno a hodnota sekvence, vcetne hlavicky. potvrďte enterem (2x):")


class Sequence:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.error = False
        self.result =   []

class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """

    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass

lines = []
while True:
    t = input()
    if not t.strip():
        break
    lines.append(t)

print("Processing...")

# 1. vezme cely text a rozdeli ho podle mezer - to jest radku, z excelu se znak pro novy radek zkopiruje jako mezera
# 2. kazdy element z toho listu priradi do promenne line
# 3. line.split("\t") rozdeli na list o dvou elementech, jmene a hodnote sekvence
# 4. Sequence(*line.split("\t")) rozprskne dva elementy do dvou parametru konstrukturu tridy Sequence a ziska instanci Sequence
# 5. promenna sequences obsahuje list instanci tridy Sequence

sequences = [Sequence(*line.split("\t")) for line in lines] # "*" unpacking
sequences = sequences[1:] # zahodime prvni radek = hlavicku


driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("https://eu.idtdna.com/calc/analyzer")
elem = driver.find_element_by_name("UserName")
elem.clear()
elem.send_keys(user)

elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys(pw)

# click Login button
elem = driver.find_element_by_id("login-button")
elem.send_keys(Keys.RETURN)

results = []
for sequence in sequences:
    print(sequence.name)

    # fill sequence
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
    elem.clear()
    elem.send_keys(sequence.value)

    # click HAIRPIN button
    hairpin_button = driver.find_elements_by_css_selector("div.sideButtons button")[1]
    hairpin_button.send_keys(Keys.RETURN)
    val = []
    # extract images
    error_text = "No structure was found for this sequence, please check again."
    try:
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#OAResults h1"), "General Information"))

    except TimeoutException:
            sequence.error = error_text
    else:
        image_div_els = driver.find_elements_by_css_selector('[data-bind = "foreach: structures"]')[0]
        #image_div_els = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-bind = "foreach: structures"]')))
        image_els = image_div_els.find_elements_by_tag_name("img")
        image_srcs = [e.get_attribute("src") for e in image_els]
        val = image_srcs

    sequence.result = val
    results.append(sequence)

tmpl = Template(Path('output_template.html').read_text())
html = tmpl.render(results=results)
output = Path('output.html')
output.write_text(html)
webbrowser.open(output)

driver.close()