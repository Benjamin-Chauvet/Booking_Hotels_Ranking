from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAMoTTjjAkgJWARoTYgBAZgBCbgBF8gBDNgBAegBAfgBA4gCAagCA7gC7IOlmwbAAgHSAiQyZjdmNDc2OS00Yjg5LTRjNjItOWE3Yi0wNTQ2YzkwOTljNmLYAgXgAgE&lang=en-gb&sid=d98fb0657b85147a603aa5741b87a9c7&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1FCAMoTTjjAkgJWARoTYgBAZgBCbgBF8gBDNgBAegBAfgBA4gCAagCA7gC7IOlmwbAAgHSAiQyZjdmNDc2OS00Yjg5LTRjNjItOWE3Yi0wNTQ2YzkwOTljNmLYAgXgAgE%26sid%3Dd98fb0657b85147a603aa5741b87a9c7%26sb_price_type%3Dtotal%26%26&ss=Paris%2C+France&is_ski_area=&ssne=Lyon&ssne_untouched=Lyon&checkin_year=&checkin_month=&checkout_year=&checkout_month=&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=-1456928&dest_type=city&search_pageview_id=007b7c295a5702a7&search_selected=true'

driver = webdriver.Chrome()
driver.get(url)


accept_cookie = driver.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]')
accept_cookie.click()

#hotels = driver.find_elements('xpath', '/html/body/div[3]/div/div[3]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[4]/div[4]/div[1]/div[2]')
#hotels = driver.find_elements(By.CLASS_NAME, 'd20f4628d0')
hotels = driver.find_elements(By.CLASS_NAME, 'a1b3f50dcd')

for hotel in hotels:
    title = hotel.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[4]/div[1]')
    print(hotel.text)
sleep(5)

#<div class="d20f4628d0">
#//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[4]/div[1]

#//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[4]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]
