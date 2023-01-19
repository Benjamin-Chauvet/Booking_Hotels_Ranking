"""Description

Librairie permettant de scraper les données des chambres d'hotels de Booking.com selon la ville et la date souhaitée.

Exemple : 
    >>> C:\path> python scraping.py Paris 15 January 2023
    Récupère les informations des chambres d'hotels de Paris trouvés sur booking.com pour la nuit du 15 Janvier 2023 pour 2 personnes.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    WebDriverException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from time import sleep
from dataclasses import dataclass, astuple
import serde.json
from typing import Tuple


@dataclass
class Room:
    """
    # Dataclass Room
    | Variable            | Type  | Description                                            |
    | ------------------- | ----- | ------------------------------------------------------ |
    | `Room_id`           | int   | Room's option ID number                                |
    | `Room_name`         | str   | Room name                                              |
    | `Room_price`        | int   | Room price for selected duration                       |
    | `Room_sleeps`       | int   | Room's option total occupancy                          |
    | `Room_promo`        | str   | Room price promotion (square meters)                   |
    | `Room_breakfast`    | str   | Room's option information about breakfast              |
    | `Room_cancellation` | str   | Room's option information about cancellation           |
    | `Room_prepayment`   | str   | Room's option information about prepayment             |
    | `Room_size`         | int   | Room's option size (square meters)                     |
    | `Hotel_id`          | str   | Hotel id                                               |
    | `Hotel_name`        | str   | Hotel name                                             |
    | `Hotel_address`     | str   | Hotel address                                          |
    | `Hotel_grade`       | float | Hotel's booking grade by consumers                     |
    | `Hotel_type`        | str   | Property type (hotel, apartement, guest house ...)     |
    | `Hotel_nb_reviews`  | int   | Hotel's number of consumers' reviews                   |
    | `Hotel_facilities`  | dict  | Hotel's facilities                                     |
    | `Hotel_stars`       | int   | Hotel's number stars                                   |
    | `Hotel_categories`  | dict  | Hotel's grades category (Staff, Comfort, Location ...) |
    """

    Room_id: int
    Room_name: str
    Room_price: int
    Room_sleeps: int
    Room_promo: str
    Room_breakfast: str
    Room_cancellation: str
    Room_prepayment: str
    Room_size: int
    Hotel_id: str
    Hotel_name: str
    Hotel_address: str
    Hotel_grade: float
    Hotel_type: str
    Hotel_nb_reviews: int
    Hotel_facilities: dict
    Hotel_stars: int
    Hotel_categories: dict


option = webdriver.ChromeOptions()
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_argument("--start-maximized")
driver = webdriver.Chrome(options=option)
try:
    driver.get("https://www.booking.com/en-gb/")
except WebDriverException:
    driver.quit()

driver.implicitly_wait(1)


def search(
    destination: str,
    checkin_date: Tuple[str, str, str],
    checkout_date: Tuple[str, str, str] = None,
):
    """
    Lance la recherche Booking selon la ville et la date souhaitée.
    """
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except NoSuchElementException:
        print("No cookies on the web page")
    try:
        search_bar = driver.find_element(By.CLASS_NAME, "sb-destination__input")
    except NoSuchElementException:
        try:
            search_bar = driver.find_element(
                By.CSS_SELECTOR, '[aria-label="Please type your destination"]'
            )
        except NoSuchElementException:
            search_bar = driver.find_element(
                By.CSS_SELECTOR, '[placeholder="Where are you going?"]'
            )
    sleep(1)
    search_bar.send_keys(destination)
    sleep(1)
    try:
        open_calendar = driver.find_element(
            By.CSS_SELECTOR, '[data-calendar2-title="Check-in"]'
        )
    except NoSuchElementException:
        try:
            open_calendar = driver.find_element(
                By.CSS_SELECTOR, '[class="xp__input-group xp__date-time"]'
            )
        except NoSuchElementException:
            open_calendar = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="date-display-field-start"]'
            )
    open_calendar.click()
    day, month, year = checkin_date
    while True:
        try:
            driver.find_element(
                By.CSS_SELECTOR,
                f"[aria-label='{day} {month} {year}']",
            ).click()
            break
        except NoSuchElementException:
            driver.find_element(
                By.CSS_SELECTOR, '[data-bui-ref="calendar-next"]'
            ).click()
    if not checkout_date:
        pass
    else:
        while True:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, f"[aria-label='{checkout_date}']"
                ).click()
                break
            except NoSuchElementException:
                driver.find_element(
                    By.CSS_SELECTOR, '[data-bui-ref="calendar-next"]'
                ).click()
    try:
        search_button = driver.find_element(By.CLASS_NAME, "xp__button")
    except NoSuchElementException:
        try:
            search_button = driver.find_element(
                By.CSS_SELECTOR, '[class="sb-searchbox__button "]'
            )
        except NoSuchElementException:
            search_button = driver.find_element(
                By.CSS_SELECTOR,
                '[class="fc63351294 a822bdf511 d4b6b7a9e7 cfb238afa1 af18dbd5a4 f4605622ad aa11d0d5cd"]',
            )
    search_button.click()
    try:
        driver.find_element(
            By.CSS_SELECTOR, "[aria-label='Dismiss sign in information.']"
        ).click()
    except NoSuchElementException:
        print("No sign in message")


def open_rooms(rooms, hotel_data, room_list):
    """
    Récupère les inforamations des différentes chambres d'un hotel.
    """
    try:
        lines = driver.find_elements(By.CSS_SELECTOR, "tr.js-rt-block-row")
    except NoSuchElementException:
        exit
    for room in range(0, len(rooms)):
        try:
            room_id = rooms[room].get_attribute("data-room-id")
        except NoSuchElementException:
            continue
        try:
            rooms[room].click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            continue
        sleep(1)
        try:
            desc_tag = driver.find_elements(
                By.CLASS_NAME, "hprt-lightbox-right-container"
            )
        except NoSuchElementException:
            try:
                desc_tag = driver.find_elements(
                    By.CLASS_NAME, "hprt-lightbox-left-container"
                )
            except NoSuchElementException:
                continue
        try:
            room_desc = desc_tag[-1].text
            room_size = room_desc.split("ize")[1].split(" m")[0]
            if len(room_size) > 4:
                room_size = room_size.split("\n")[-1]
        except IndexError:
            room_size = ""
        try:
            driver.find_element(By.CLASS_NAME, "modal-mask-closeBtn").click()
        except NoSuchElementException:
            try:
                driver.find_element(By.CLASS_NAME, "bui-modal__close").click()
            except NoSuchElementException:
                try:
                    elements = driver.find_elements(
                        By.CSS_SELECTOR, '[id="hp_rt_room_gallery_modal_room_name"]'
                    )
                    elem = elements[-1]
                    ac = ActionChains(driver)
                    try:
                        ac.move_to_element(elem).move_by_offset(
                            0, 650
                        ).click().perform()
                    except ElementNotInteractableException:
                        try:
                            ac.move_to_element(elem).move_by_offset(
                                600, 0
                            ).click().perform()
                        except ElementNotInteractableException:
                            pass
                except (IndexError, NameError):
                    pass
        for line in lines:
            try:
                room_full_id = line.get_attribute("data-block-id")
                room_id_1 = room_full_id.split("_")[0]
            except (NoSuchElementException, AttributeError):
                continue
            if room_id_1 == room_id:
                room_name = driver.find_element(
                    By.CSS_SELECTOR, f'a[data-room-id="{room_id_1}"]'
                ).text
                room_price = (
                    driver.find_element(
                        By.CSS_SELECTOR, f'[data-block-id="{room_full_id}"]'
                    )
                    .find_element(By.CLASS_NAME, "prco-valign-middle-helper")
                    .text
                )
                room_sleeps = (
                    driver.find_element(
                        By.CSS_SELECTOR, f'[data-block-id="{room_full_id}"]'
                    )
                    .find_element(By.CLASS_NAME, "bui-u-sr-only")
                    .text[-1]
                )
                try:
                    room_promo = driver.find_element(
                        By.CSS_SELECTOR,
                        '[class="bui-badge bui-badge--constructive"]',
                    ).text
                except NoSuchElementException:
                    room_promo = ""
                try:
                    room_breakfast = line.find_element(
                        By.CSS_SELECTOR, '[class="bui-list__description"]'
                    ).text
                except NoSuchElementException:
                    room_breakfast = ""
                try:
                    room_cancellation = line.find_element(
                        By.CSS_SELECTOR, '[data-testid="cancellation-subtitle"]'
                    ).text
                except NoSuchElementException:
                    room_cancellation = ""
                try:
                    room_prepayment = line.find_element(
                        By.CSS_SELECTOR, '[data-testid="prepayment-subtitle"]'
                    ).text
                except NoSuchElementException:
                    room_prepayment = ""
                room_data = Room(
                    room_full_id,
                    room_name,
                    room_price,
                    room_sleeps,
                    room_promo,
                    room_breakfast,
                    room_cancellation,
                    room_prepayment,
                    room_size,
                    *hotel_data,
                )
                room_list.append(room_data)
            return room_list


def open_hotels(hotels: list, room_list: list) -> list:
    """
    Récupère les informations sur tous les hotels d'une page ainsi que leurs différentes chambres associées.
    """
    main_page = driver.window_handles[0]
    for hotel in range(0, len(hotels)):
        try:
            hotels[hotel].click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            sleep(4)
            hotels[hotel].click()
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        try:
            hotel_id_tag = driver.find_element(
                By.CSS_SELECTOR,
                '[class="txp-sidebar-block hp-lists hp-lists--save-wl-below-ph hide"]',
            )
            hotel_id = hotel_id_tag.get_attribute("data-hotel-id")
        except NoSuchElementException:
            hotel_id = ""
        try:
            hotel_name = driver.find_element(
                By.CSS_SELECTOR, "h2[class='d2fee87262 pp-header__title']"
            ).text
        except NoSuchElementException:
            hotel_name = ""
        try:
            hotel_address = driver.find_element(
                By.CSS_SELECTOR, "span[data-node_tt_id='location_score_tooltip']"
            ).text
        except NoSuchElementException:
            hotel_address = ""
        try:
            hotel_grade = driver.find_element(
                By.CSS_SELECTOR, "div[class='b5cd09854e d10a6220b4']"
            ).text
        except NoSuchElementException:
            hotel_grade = ""
        try:
            hotel_type = driver.find_element(
                By.CSS_SELECTOR, "span[data-testid='property-type-badge']"
            ).text
        except NoSuchElementException:
            hotel_type = ""
        try:
            hotel_nb_reviews = driver.find_element(
                By.CSS_SELECTOR, "span[class='b5cd09854e c90c0a70d3 db63693c62']"
            ).text
        except NoSuchElementException:
            hotel_nb_reviews = ""
        try:
            facilities_categories = driver.find_elements(
                By.CSS_SELECTOR, 'div[class="hotel-facilities-group"]'
            )
            hotel_facilities = {}
            for i in range(0, len(facilities_categories)):
                facility_category = facilities_categories[i].text.split("\n")[0]
                hotel_facilities[f"{facility_category}"] = facilities_categories[
                    i
                ].text.split("\n")[1:]
        except NoSuchElementException:
            hotel_facilities = {}
        try:
            nb_stars = driver.find_elements(
                By.CSS_SELECTOR, "span[class='b6dc9a9e69 adc357e4f1 fe621d6382']"
            )
            hotel_nb_stars = len(nb_stars)
        except NoSuchElementException:
            hotel_nb_stars = 0
        try:
            rate_categories = driver.find_elements(
                By.CSS_SELECTOR, 'div[data-testid="review-subscore"]'
            )
            hotel_categories = {}
            for i in range(0, len(rate_categories)):
                category = rate_categories[i].text.split("\n")[0]
                hotel_categories[f"{category}"] = rate_categories[i].text.split("\n")[
                    1:
                ]
            try:
                del hotel_categories[""]
            except KeyError:
                pass
        except NoSuchElementException:
            hotel_categories = {}
        try:
            rooms = driver.find_elements(By.CLASS_NAME, "hprt-roomtype-link")
        except NoSuchElementException:
            continue
        hotel_data = [
            hotel_id,
            hotel_name,
            hotel_address,
            hotel_grade,
            hotel_type,
            hotel_nb_reviews,
            hotel_facilities,
            hotel_nb_stars,
            hotel_categories,
        ]
        open_rooms(rooms, hotel_data, room_list)
        driver.close()
        driver.switch_to.window(main_page)
    return room_list


def collect_data(destination: str, checkin_date: Tuple[int, str, int]):
    """
    Fonction retournant les données brutes au format json après avoir lancé la recherche Booking avec la fonction search()
    et récupéré les informations sur la totalité des pages d'hotels en utilisant la fonction open_hotels().
    """
    search(destination, checkin_date)
    room_list = []
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except NoSuchElementException:
        print("No cookies on the web page")
    # while int(driver.find_element(By.CLASS_NAME, "cfc6afb67a").text.split()[-1]) < 1000:
    hotels = driver.find_elements(By.CLASS_NAME, "a23c043802")
    open_hotels(hotels[0:2], room_list)
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").click()
    sleep(2)
    driver.quit()
    json_data = serde.json.to_json(room_list)
    with open(f"Booking_Hotels.json", "w") as fichier:
        fichier.write(json_data)
