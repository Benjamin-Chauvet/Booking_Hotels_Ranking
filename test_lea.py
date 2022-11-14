from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()
driver.get('https://www.booking.com')


#accepte les cookies
driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
sleep(2)
#écrit Paris dans la barre de recherche
search_bar = driver.find_element(By.CLASS_NAME, "sb-destination-label-sr")
search_bar.send_keys('Paris')


#clique sur rechercher
search_bouton = driver.find_element(By.CLASS_NAME, 'xp__button')
search_bouton.click()
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



