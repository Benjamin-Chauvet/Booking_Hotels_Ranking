"""Description

Librairie permettant de scraper les données des hotels booking.com de la ville souhaitée à la date souhaitée.

Exemple : 
    >>> C:\path> python destination.py Londres 11 December 2022
    Récupère les informations de tous les hotels de Londres trouvés sur booking.com pour la nuit du 11 Décembre 2022 pour 2 personnes.
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, StaleElementReferenceException
from time import sleep
import pandas as pd
import sys
from dataclasses import dataclass
from serde.json import to_json

@dataclass
class Room:
    Room_id: int
    Room_name: str
    Room_price: int
    Room_sleeps: int
    Room_promo: str
    Room_breakfast: str
    Room_cancellation: str
    Room_prepayment: str
    Room_size: int
    Hotel_Name: str
    Hotel_address: str
    Hotel_grade: float
    Hotel_type: str
    Hotel_nb_reviews: int
    Hotel_facilities: dict
    Hotel_stars: int
    Hotel_categories: dict

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

checkin_date = '15 January 2023'
checkout_date = None
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, f"[aria-label='{checkin_date}']").click()
        break
    except NoSuchElementException:
        driver.find_element(By.CSS_SELECTOR, '[data-bui-ref="calendar-next"]').click()

if not checkout_date:
    pass
else:
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, f"[aria-label='{checkout_date}']").click()
            break
        except NoSuchElementException:
            driver.find_element(By.CSS_SELECTOR, '[data-bui-ref="calendar-next"]').click()

try:
    search_bouton = driver.find_element(By.CLASS_NAME, 'xp__button')
except NoSuchElementException:
    pass
search_bouton.click()

try:
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Dismiss sign in information.']").click()
except NoSuchElementException:
    print('No sign in message')

main_page = driver.window_handles[0]

def open_hotels(hotels, room_list):
    """Récupère les backups html des hotels d'une page."""
    for hotel in range(0, len(hotels)):
        try:
            hotels[hotel].click()
        except StaleElementReferenceException or ElementClickInterceptedException:
            continue
        sleep(2)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        try:
            hotel_name = driver.find_element(By.CSS_SELECTOR, "h2[class='d2fee87262 pp-header__title']").text
        except NoSuchElementException:
            hotel_name = ''
        try:
            hotel_address = driver.find_element(By.CSS_SELECTOR, "span[data-node_tt_id='location_score_tooltip']").text
        except NoSuchElementException:
            hotel_address = ''
        try:
            hotel_grade = driver.find_element(By.CSS_SELECTOR, "div[class='b5cd09854e d10a6220b4']").text
        except NoSuchElementException:
            hotel_grade = ''
        try:
            hotel_type = driver.find_element(By.CSS_SELECTOR, "span[data-testid='property-type-badge']").text
        except NoSuchElementException:
            hotel_type = ''
        try:
            hotel_nb_reviews = driver.find_element(By.CSS_SELECTOR, "span[class='b5cd09854e c90c0a70d3 db63693c62']").text
        except NoSuchElementException:
            hotel_nb_reviews = ''
        #hotel_facilities = driver.find_element(By.CSS_SELECTOR, "div[data-et-view='goal:hp_d_property_popular_facilities_seen']").text
        try:
            facilities_categories = driver.find_elements(By.CSS_SELECTOR, 'div[class="hotel-facilities-group"]')
            hotel_facilities = {}
            for i in range(0, len(facilities_categories)):
                facility_category = facilities_categories[i].text.split("\n")[0]
                hotel_facilities[f'{facility_category}'] = facilities_categories[i].text.split("\n")[1:]
        except NoSuchElementException:
            hotel_facilities = {}
        try:
            nb_stars = driver.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
            hotel_nb_stars = len(nb_stars)
        except NoSuchElementException:
            hotel_nb_stars = ''
        try:
            rate_categories = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="review-subscore"]')
            hotel_categories={}
            for i in range(0, len(rate_categories)):
                category = rate_categories[i].text.split("\n")[0]
                hotel_categories[f'{category}'] = rate_categories[i].text.split("\n")[1:]
            del hotel_categories[""]
        except NoSuchElementException:
            hotel_categories={}
        #hotel_data = Hotel(hotel_name, hotel_adress, hotel_grade, hotel_type, hotel_nb_reviews, len(nb_stars), hotel_facilities)
        try:
            rooms = driver.find_elements(By.CLASS_NAME, "hprt-roomtype-link")
        except NoSuchElementException:
            continue
        try:
            lines = driver.find_elements(By.CSS_SELECTOR, 'tr.js-rt-block-row')
        except NoSuchElementException:
            continue
        for room in range(0, len(rooms)):
            try:
                room_id = rooms[room].get_attribute("data-room-id")
            except NoSuchElementException:
                continue
            try:
                rooms[room].click()
            except ElementClickInterceptedException:
                continue
            sleep(2)
            try:
                desc_tag = driver.find_elements(By.CLASS_NAME, "hprt-lightbox-cleanup")
            except NoSuchElementException:
                continue
            try:
                room_desc = desc_tag[-1].text
                room_size = room_desc.split('ize ')[1].split(' m')[0]
            except IndexError:
                room_size = ''
            try:
                driver.find_element(By.CLASS_NAME, "modal-mask-closeBtn").click()
            except NoSuchElementException:
                pass
                #driver.find_element(By.CLASS_NAME, "bui-modal__close").click()
            for line in lines:
                try:
                    room_id_1 = line.get_attribute("data-block-id")
                    room_id_1 = room_id_1.split("_")[0]
                    if room_id_1 == room_id:
                        room_full_id = line.get_attribute("data-block-id")
                        room_name = driver.find_element(By.CSS_SELECTOR, f'a[data-room-id="{room_id_1}"]').text
                        room_price = driver.find_element(By.CSS_SELECTOR, f'[data-block-id="{room_full_id}"]').find_element(By.CLASS_NAME, "prco-valign-middle-helper").text
                        room_sleeps = driver.find_element(By.CSS_SELECTOR, f'[data-block-id="{room_full_id}"]').find_element(By.CLASS_NAME, "bui-u-sr-only").text[-1]
                        try:
                            room_promo = driver.find_element(By.CSS_SELECTOR, '[class="bui-badge bui-badge--constructive"]').text
                        except NoSuchElementException:
                            room_promo = ''
                        try:
                            room_breakfast = line.find_element(By.CSS_SELECTOR, '[class="bui-list__description"]').text
                        except NoSuchElementException:
                            room_breakfast = ''
                        try:
                            room_cancellation = line.find_element(By.CSS_SELECTOR, '[data-testid="cancellation-subtitle"]').text
                        except NoSuchElementException:
                            room_cancellation = ''
                        try:
                            room_prepayment = line.find_element(By.CSS_SELECTOR, '[data-testid="prepayment-subtitle"]').text
                        except NoSuchElementException:
                            room_prepayment = ''
                        room_data = Room(room_full_id,
                            room_name,
                            room_price,
                            room_sleeps,
                            room_promo,
                            room_breakfast,
                            room_cancellation,
                            room_prepayment,
                            room_size,
                            hotel_name,
                            hotel_address,
                            hotel_grade,
                            hotel_type,
                            hotel_nb_reviews,
                            hotel_facilities,
                            hotel_nb_stars,
                            hotel_categories)
                        room_list.append(room_data)
                #except NoSuchElementException:
                except NoSuchElementException or AttributeError:
                    #room_name = line.find_element(By.CLASS_NAME, "hprt-roomtype-icon-link ").text
                    continue
                    """room_id_1 = ''
                    room_full_id = ''
                    room_name = ''
                    room_price = ''
                    room_sleeps = ''
                    room_choices = ''
                    room_promo = ''
                    room_data = Room(room_full_id,
                            room_name,
                            room_price,
                            room_sleeps,
                            room_choices,
                            room_promo,
                            room_size,
                            hotel_name,
                            hotel_adress,
                            hotel_grade,
                            hotel_type,
                            hotel_nb_reviews,
                            hotel_facilities,
                            hotel_nb_stars,
                            hotel_categories)
                    room_list.append(room_data)"""
                #room_name = driver.find_element(By.CSS_SELECTOR, f'[data-block-id="{room_id}_{room_id_3}"]').find_element(By.CLASS_NAME, "hprt-roomtype-icon-link ").text
        #rooms = driver.find_elements(By.CLASS_NAME, "hprt-roomtype-icon-link ")
        #open_rooms(rooms)
        driver.close()
        driver.switch_to.window(main_page)
    return room_list

def scrap_hotels():
    """Permet de naviguer sur l'ensemble des pages et d'en récupérer les backups avec la fonction open_hotels."""
    room_list = []
    try:
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    except NoSuchElementException:
        print('No cookies on the web page')
    while int(driver.find_element(By.CLASS_NAME, "cfc6afb67a").text.split()[-1]) < 1000:
        hotels = driver.find_elements(By.CLASS_NAME, 'a23c043802')
        open_hotels(hotels, room_list)
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").click()
        sleep(1)
    driver.quit()
    return room_list

def collect_backups():
    data = scrap_hotels()
    df = pd.DataFrame(data)
    df.to_csv(f'hotels_booking_'+destination+'_py.csv')
    return df

def collect_backups():
    json_data = to_json(scrap_hotels())
    with open(f'hotels_'+destination+'_1000.json', 'w') as fichier:
        fichier.write(json_data)

collect_backups()