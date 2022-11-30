"""Description

Librairie permettant de scraper les données des hotels de la ville souhaitée sur booking.com

Exemple : 
    >>> C:\path> python destination.py Londres
    Récupère les informations de tous les hotels de Londres trouvés sur booking.com pour la période 't à t+1' pour 2 personnes.
"""

# A généraliser

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import sys

option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("--start-maximized")
driver = webdriver.Chrome(options=option)
driver.get('https://www.booking.com/en-gb/')

driver.implicitly_wait(10)

try:
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
except:
    print('No cookies on the web page')

destination = "Paris"
try:
    search_bar = driver.find_element(By.CLASS_NAME, "sb-destination-label-sr")
except:
    search_bar = driver.find_element(By.CLASS_NAME, "ce45093752")
sleep(1)
search_bar.send_keys(destination) # attention il faudra traiter si on veut "Paris" ou "Paris centre"
sleep(1)

try:
    open_calendar = driver.find_element(By.CLASS_NAME, "xp__dates-inner")
except:
    open_calendar = driver.find_element(By.CLASS_NAME, "d67d113bc3")
open_calendar.click()
desired_date = '30 November 2022'
driver.find_element(By.CSS_SELECTOR, f"[aria-label='{desired_date}']").click()

try:
    search_bouton = driver.find_element(By.CLASS_NAME, 'xp__button')
except:
    search_bouton = driver.find_element(By.CLASS_NAME, 'e57ffa4eb5')
search_bouton.click()

try:
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Dismiss sign in information.']").click()
except:
    print('No sign in message')

main_page = driver.window_handles[0]

def open_rooms(rooms):
    main_window = driver.current_url
    for room in range(0, len(rooms)):
        rooms[room].click()
        sleep(2)
        #room_window = driver.window_handles[1]
        #driver.switch_to.window(room_window)
        #hotel_desc = driver.find_element('xpath', '//*[@id="blocktoggleRD24344202"]/div[1]/div/div[2]').text
        #hotel_desc = driver.find_element(By.CLASS_NAME, "hprt-lightbox-right-container hprt-lightbox-cleanuphprt-lightbox-right-container hprt-lightbox-cleanup").text
        #hotel_desc = driver.find_element(By.CSS_SELECTOR, "#blocktoggleRD49419507 > div.room-lightbox-container.js-async-room-lightbox-container > div > div.hprt-lightbox-right-container.hprt-lightbox-cleanup").text
        desc_tag = driver.find_elements(By.CLASS_NAME, "hprt-lightbox-cleanup")
        """if len(desc_tag) == 1:
            room_desc = desc_tag[0].text
        else:   
            room_desc = desc_tag[-1].text"""
        room_desc = desc_tag[-1].text
        try:
            sqft = room_desc.split('size ')[1].split(' m')[0]
        except:
            sqft = room_desc.split('Size ')[1].split(' m')[0]
        print(sqft)
        bed_type = driver.find_element(By.CLASS_NAME, 'rt-bed-type').text
        print(bed_type)
        driver.find_element(By.CLASS_NAME, "modal-mask-closeBtn").click() # close hotel desc
        #driver.switch_to.window(main_window)


def open_hotels(hotels):
    """Récupère les backups html des hotels d'une page."""
    for hotel in range(0, len(hotels)):
        hotels[hotel].click()
        sleep(2)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        name = driver.find_element(By.CLASS_NAME, "pp-header__title").text
        print(name) # Mettre code pour scrap données par hotel (Ici récupère nom des hotels)
        request = get(driver.current_url)
        soupe = BeautifulSoup(request.text, features = 'lxml')
        grade = soupe.find(class_ = "b5cd09854e d10a6220b4").text
        print(grade)
        rating_stars = len(soupe.find_all(class_ = "b6dc9a9e69 adc357e4f1 fe621d6382"))
        print(rating_stars)
        rooms = driver.find_elements(By.CLASS_NAME, "hprt-roomtype-icon-link ")
        open_rooms(rooms)
        driver.close()
        driver.switch_to.window(main_page)

def scrap_hotels():
    """Permet de naviguer sur l'ensemble des pages et d'en récupérer les backups avec la fonction open_hotels."""
    try:
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    except:
        print('No cookies on the web page')
    while int(driver.find_element(By.CLASS_NAME, "cfc6afb67a").text.split()[-1]) < 1000:
        hotels = driver.find_elements(By.CLASS_NAME, 'a23c043802')
        open_hotels(hotels)
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").click()
        #driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[6]/div[2]/nav/div/div[3]/button').click() xpath a changé
        sleep(1)

scrap_hotels()