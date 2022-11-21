"""Description.

Librairie pour récupérer les backups html des hotels du site de Booking d'une ville donnée.
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAMoTTjjAkgJWARoTYgBAZgBCbgBF8gBDNgBAegBAfgBA4gCAagCA7gC7IOlmwbAAgHSAiQyZjdmNDc2OS00Yjg5LTRjNjItOWE3Yi0wNTQ2YzkwOTljNmLYAgXgAgE&lang=en-gb&sid=d98fb0657b85147a603aa5741b87a9c7&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1FCAMoTTjjAkgJWARoTYgBAZgBCbgBF8gBDNgBAegBAfgBA4gCAagCA7gC7IOlmwbAAgHSAiQyZjdmNDc2OS00Yjg5LTRjNjItOWE3Yi0wNTQ2YzkwOTljNmLYAgXgAgE%26sid%3Dd98fb0657b85147a603aa5741b87a9c7%26sb_price_type%3Dtotal%26%26&ss=Paris%2C+France&is_ski_area=&ssne=Lyon&ssne_untouched=Lyon&checkin_year=&checkin_month=&checkout_year=&checkout_month=&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=-1456928&dest_type=city&search_pageview_id=007b7c295a5702a7&search_selected=true'
driver = webdriver.Chrome()
driver.get(url)

destination = 'Paris'  # 
main_page = driver.window_handles[0]

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
        driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[5]/div[2]/nav/div/div[3]/button').click()
        sleep(1)

scrap_hotels()

"""def collect_backups(url): Récupère les backups html en appelant la fonction scrap_hotels et les enregistre au format csv.
    
    data = scrap_hotels(destination)
    df = pd.DataFrame(data)
    df.to_csv(f'hotels_booking_'+destination+'.csv')
    return df

collect_backups(url)"""
