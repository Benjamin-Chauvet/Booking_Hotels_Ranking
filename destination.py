"""Description

Librairie permettant de scraper les données des hotels de la ville souhaitée sur booking.com

Exemple : 
    >>> C:\path> python destination.py Londres
    Récupère les informations de tous les hotels de Londres trouvés sur booking.com pour la période 't à t+1' pour 2 personnes.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import sys

def voyage(destination):
    driver = webdriver.Chrome()
    driver.get('https://www.booking.com')
    sleep(2)
    try:
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    except:
        print('No cookies on the web page')
    sleep(3)

    search_bar = driver.find_element(By.CLASS_NAME, "sb-destination-label-sr")
    sleep(1)
    search_bar.send_keys(destination)
    sleep(1)

    open_calendar = driver.find_element(By.CLASS_NAME, "xp__dates-inner")
    open_calendar.click()
    sleep(2)
    month_find = driver.find_element(By.CLASS_NAME, "bui-calendar__month")
    month, year = month_find.text.split()
    if month == sys.argv[2] and year == sys.argv[3]:
        # bon mois de la bonne année
        print("Bonne date recherchée:", sys.argv[2], sys.argv[3])
    else:
        next_month = driver.find_element('xpath', '//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]/svg')
        while month != sys.argv[2]:
            next_month.click()
            month_find = driver.find_element(By.CLASS_NAME, "bui-calendar__month")
            month, year = month_find.text.split()
            print(month, year)

    #for month in month_find:
        #print(month)

        """
        if month.text.split()[0] == sys.argv[2]:
            # on peut choisir le jour dans ce mois
            print("go scrap décembre")
        else:
            next_month = driver.find_element('xpath', '//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[2]/svg')
            next_month.click()
            next_month.click()
            month_find = driver.find_elements(By.CLASS_NAME, "bui-calendar__month")
"""
    """
    select_checkin_date = driver.find_element('xpath', '//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/table/tbody/tr[4]/td[6]')
    select_checkout_date = driver.find_element('xpath', '//*[@id="frm"]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/table/tbody/tr[4]/td[7]')
    select_checkin_date.click()
    select_checkout_date.click()
    sleep(2)"""

    search_bouton = driver.find_element(By.CLASS_NAME, 'xp__button')
    search_bouton.click()

    sleep(5)

voyage(sys.argv[1])

#voyage("Londres")


#selectionne la durée du séjour
#open_calendar = driver.find_element(By.CLASS.NAME, "xp__dates-inner")
#open_calendar.click()

#select_date = driver.find_element(By.CLASS_NAME, "bui-calendar__date")
#select_date.click()

#clique sur rechercher
"""
sleep(2)
new_url = driver.current_url
driver.get(new_url)
sleep(2)

#accepte les cookies
#driver.find_element(By.CLASS_NAME, 'bb0b3e18ca bad25cd8dc d9b0185ac2 ba6d71e9d5').click()

#clique sur le premier hôtel
#driver.find_element(By.CLASS_NAME, 'd20f4628d0').click()
#driver.find_element(By.CLASS_NAME, 'a1b3f50dcd').click()
click_first_hotel = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[3]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]')
click_first_hotel.click()

#récupère le nouvel url, réouvre la page avec cet url et la referme
new_url_bis = driver.current_url
driver.get(new_url_bis)
driver.switch_to.window(driver.window_handles[1])
driver.close()
"""


