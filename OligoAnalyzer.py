from time import sleep

import webbrowser
import datetime as dt

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from jinja2 import Template
from pathlib import Path
from configparser import ConfigParser, NoOptionError

user = ""
pw = ""
param_set = "qPCR"
target_type = "RNA"
oligo_conc = 0.2
na_conc = 50
mg_conc = 3
dntps_conc = 0.8
temp = 40

ini = Path("user.ini")
if ini.exists():
    config = ConfigParser()
    config.read(ini)
    for k in config.options("main"):
        try:
            if k in locals():
                locals()[k] = config.get("main", k)
        except NoOptionError:
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
        self.result = []


lines = []
while True:
    t = input()
    if not t.strip():
        break
    lines.append(t)

# 1. vezme cely text a rozdeli ho podle mezer - to jest radku, z excelu se znak pro novy radek zkopiruje jako mezera
# 2. kazdy element z toho listu priradi do promenne line
# 3. line.split("\t") rozdeli na list o dvou elementech, jmene a hodnote sekvence
# 4. Sequence(*line.split("\t")) rozprskne dva elementy do dvou parametru konstrukturu tridy Sequence a ziska instanci Sequence
# 5. promenna sequences obsahuje list instanci tridy Sequence

sequences = [Sequence(*line.split(":")) for line in lines] # "*" unpacking
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
elem.click()

# wait until logged in
try:
    WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
except TimeoutException:
    print("Invalid login?")
    driver.close()
    exit()

print("Processing...")

results = []
for sequence in sequences:
    print(sequence.name)

    # fill sequence
    elem = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
    elem.clear()
    elem.send_keys(sequence.value)

    # fill parameters set
    elem = driver.find_elements_by_xpath('//option[contains(., "'+ param_set +'")] ')[0]
    elem.click()

    # fill target type
    elem = driver.find_elements_by_xpath('//option[contains(., "'+ target_type +'")] ')[0]
    elem.click()

    # fill oligo concentration
    elem = driver.find_element_by_xpath('//input[@data-bind="value: oligoConc"]')
    elem.clear()
    elem.send_keys(oligo_conc)

    # fill na concentration
    elem = driver.find_element_by_xpath('//input[@data-bind="value: naConc"]')
    elem.clear()
    elem.send_keys(na_conc)

    # fill mg concentration
    elem = driver.find_element_by_xpath('//input[@data-bind="value: mgConc"]')
    elem.clear()
    elem.send_keys(mg_conc)

    # fill dNTPs concentration
    elem = driver.find_element_by_xpath('//input[@data-bind="value: dNTPsConc"]')
    elem.clear()
    elem.send_keys(dntps_conc)

    # click HAIRPIN button
    hairpin_button = driver.find_elements_by_css_selector("div.sideButtons button")[1]
    hairpin_button.click()
    val = []

    # Wait for General Information:
    error_text = "No structure was found for this sequence, please check again."
    try:
        WebDriverWait(driver, 3).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#OAResults h1"), "General Information"))
    except TimeoutException:
        sequence.error = error_text
    else:
        # fill in temperature
        elem = driver.find_element_by_xpath('//input[@data-bind="value: temp"]')
        elem.clear()
        elem.send_keys(temp)
        # click Update button
        update_button = driver.find_elements_by_css_selector(".UnafoldInputs button")[0]
        update_button.click()


        # extract images
        error_text = "No structure was found for this sequence, please check again."
        try:
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#OAResults h1"), "General Information"))
        except TimeoutException:
                sequence.error = error_text
        else:
            image_div_els = driver.find_elements_by_css_selector('[data-bind = "foreach: structures"]')[0]
            image_els = image_div_els.find_elements_by_tag_name("img")
            image_srcs = [e.get_attribute("src") for e in image_els]
            val = image_srcs

        sequence.result = val
        results.append(sequence)

print("Generating report...")
print("(note that images included in the report are temporarily saved on the server")
print(" - you might want to save a copy of the report before they are deleted")

tmpl = Template(Path('output_template.html').read_text())
html = tmpl.render(results=results)
now = dt.datetime.now()
output = Path(f'output_{now.strftime("%Y%m%d_%H%M%S")}.html')
output.write_text(html)
webbrowser.open(output)


driver.close()