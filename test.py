from selenium import webdriver
from selenium.webdriver.common.by import By

nav = webdriver.Chrome(executable_path=r'C:\Users\lele1\OneDrive - Université de Tours\M2\Machine Learning\chromedriver.exe')
nav.get('https://www.booking.com')
nav.implicitly_wait(20)

#accepte les cookies
nav.find_element(By.ID, 'onetrust-accept-btn-handler').click()

#écrit Paris dans la barre de recherche
search_bar = nav.find_element(By.CLASS_NAME, "sb-destination-label-sr")
search_bar.send_keys('Paris')

#clique sur rechercher
search_bouton = nav.find_element(By.CLASS_NAME, 'xp__button')
search_bouton.click()

new_url = nav.current_url
nav.get('new_url')
nav.implicitly_wait(20)

#accepte les cookies
nav.find_element(By.CLASS_NAME, 'bb0b3e18ca bad25cd8dc d9b0185ac2 ba6d71e9d5').click()

#clique sur le premier hôtel
nav.find_element(By.CLASS_NAME, 'd20f4628d0').click()

#récupère le nouvel url, réouvre la page avec cet url et la referme
#new_url = nav.current_url
#nav.get(new_url)
#nav.switch_to.window(nav.window_handles[1])
#nav.close()



