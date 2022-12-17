"""Description

Librairie permettant de scraper les données des hotels booking.com de la ville souhaitée à la date souhaitée.

Exemple : 
    >>> C:\path> python destination.py Londres 11 December 2022
    Récupère les informations de tous les hotels de Londres trouvés sur booking.com pour la nuit du 11 Décembre 2022 pour 2 personnes.
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import sys

option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("--start-maximized")
driver = webdriver.Chrome(options=option)
try:
    driver.get('https://www.booking.com/en-gb/')
except WebDriverException:
    print("Internet disconnected")
    driver.quit()

driver.implicitly_wait(4)


try:
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
except NoSuchElementException:
    print('No cookies on the web page')

destination = 'Paris'
try:
    search_bar = driver.find_element(By.CLASS_NAME, "sb-destination-label-sr")
    #search_bar = driver.find_element(By.CLASS_NAME, "ce45093752")
except NoSuchElementException:
    pass
sleep(1)
search_bar.send_keys(destination) # attention il faudra traiter si on veut "Paris" ou "Paris centre"
sleep(1)

try:
    open_calendar = driver.find_element(By.CLASS_NAME, "xp__dates-inner")
except NoSuchElementException:
    pass
open_calendar.click()
desired_date = '30 December 2022'
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, f"[aria-label='{desired_date}']").click()
        break
    except NoSuchElementException:
        driver.find_element(By.CSS_SELECTOR, '[data-bui-ref="calendar-next"]').click()

try:
    search_bouton = driver.find_element(By.CLASS_NAME, 'xp__button')
    #search_bouton = driver.find_element(By.CLASS_NAME, 'e57ffa4eb5')
except NoSuchElementException:
    pass
search_bouton.click()

try:
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Dismiss sign in information.']").click()
except NoSuchElementException:
    print('No sign in message')

main_page = driver.window_handles[0]

def open_rooms(rooms):
    main_window = driver.current_url
    for room in range(0, len(rooms)):
        sleeps = driver.find_element(By.CLASS_NAME, "bui-u-sr-only").text
        nb_couchage = 0
        for sleep in range(0, len(sleeps)):
            nb_couchage += 1
        print(nb_couchage)
        rooms[room].click()
        sleep(2)
        sleep_number = driver.find_element(By.CLASS_NAME, "jq_tooltip")
        for sleep in range(0, len(sleep_number)):
            sleep += 1
        print("nombre de couchage", sleep)
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
            sqft = room_desc.split('ize ')[1].split(' m')[0]
        except IndexError:
            pass
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
    except NoSuchElementException:
        print('No cookies on the web page')
    while int(driver.find_element(By.CLASS_NAME, "cfc6afb67a").text.split()[-1]) < 50:
        hotels = driver.find_elements(By.CLASS_NAME, 'a23c043802')
        open_hotels(hotels)
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").click()
        #driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[6]/div[2]/nav/div/div[3]/button').click() xpath a changé
        sleep(1)
    driver.quit()

scrap_hotels()