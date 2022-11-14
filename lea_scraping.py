from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

#récupérer les infos sur la page de l'hotel 1
requete = get('https://www.booking.com/hotel/fr/austin-s-arts-et-metiers.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaE2IAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AvnMyZsGwAIB0gIkNTcwZTYyNjktNTZjMy00YTBjLTk5YjctMmVlZDA5OGEzNzFh2AIG4AIB&sid=7ba9f340e388bcc1c3db52ff34b02dd7&all_sr_blocks=24344202_356744597_2_2_0;checkin=2022-11-26;checkout=2022-11-27;dest_id=-1456928;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=2;highlighted_blocks=24344202_356744597_2_2_0;hpos=2;matching_block_id=24344202_356744597_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=24344202_356744597_2_2_0__28936;srepoch=1668441731;srpvid=c65070c0d1a70164;type=total;ucfs=1&#hotelTmpl')
if requete.status_code == 200:
    soupe = BeautifulSoup(requete.text, features = 'lxml')
    
#Nom de l'hotel - fonctionne
names = soupe.find_all(class_ = "d2fee87262 pp-header__title")

#Adresse (rue, arr et code postal) - fonctionne 
adresses = soupe.find_all(class_ = "hp_address_subtitle js-hp_address_subtitle jq_tooltip")

#Nom chambres - fonctionne pas
room_names = soupe.find_all(class_ = "hprt-roomtype-block hprt-roomtype-name hp_rt_room_name_icon__container")


    
#for name, adresse in zip(names,adresses):
    #print(name.text, adresse.text)