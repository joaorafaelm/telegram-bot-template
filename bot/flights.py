import os
import sys
import logging
from time import sleep
from parsel import Selector
from urllib.parse import quote 
from functools import lru_cache
from webbot import Browser as WebBotBrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_SSL_VERIFY'] = '0'


class Browser(WebBotBrowser):
    def __init__(self, showWindow=True):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--disk-cache-dir=/tmp/selenium')
        options.add_argument("user-data-dir=/tmp/selenium")
        options.add_experimental_option(
            "prefs", {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            }
        )
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--blink-settings=imagesEnabled=false')

        if not showWindow:
            options.headless = True
            options.add_argument("--headless")

        drive_manager = ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=30)).install()
        service = ChromeService(drive_manager)
        self.driver = webdriver.Chrome(service=service, options=options)

        # patch deprecated method
        # .find_element_by_class_name(
        # .find_element(By.CLASS_NAME, 

        # .find_element_by_css_selector(
        # .find_element(By.CSS_SELECTOR, 

        # .find_element_by_id(
        # .find_element(By.ID, 

        # .find_element_by_link_text(
        # .find_element(By.LINK_TEXT, 

        # .find_element_by_name(
        # .find_element(By.NAME, 

        # .find_element_by_partial_link_text(
        # .find_element(By.PARTIAL_LINK_TEXT, 

        # .find_element_by_tag_name(
        # .find_element(By.TAG_NAME, 

        # .find_element_by_xpath(
        # .find_element(By.XPATH, 

        # .find_elements_by_class_name(
        # .find_elements(By.CLASS_NAME, 

        # .find_elements_by_css_selector(
        # .find_elements(By.CSS_SELECTOR, 

        # .find_elements_by_id(
        # .find_elements(By.ID, 

        # .find_elements_by_link_text(
        # .find_elements(By.LINK_TEXT, 

        # .find_elements_by_name(
        # .find_elements(By.NAME, 

        # .find_elements_by_partial_link_text(
        # .find_elements(By.PARTIAL_LINK_TEXT, 

        # .find_elements_by_tag_name(
        # .find_elements(By.TAG_NAME, 

        # .find_elements_by_xpath(
        # .find_elements(By.XPATH,
        self.driver.find_elements_by_xpath = lambda x: self.driver.find_elements(By.XPATH, x)
        self.driver.find_elements_by_link_text = lambda x: self.driver.find_elements(By.LINK_TEXT, x)

        self.Key = Keys
        self.errors = []

        [setattr(self, function, getattr(self.driver, function)) for function in
         ['add_cookie', 'delete_all_cookies', 'delete_cookie', 'execute_script', 'execute_async_script',
          'fullscreen_window', 'get_cookie', 'get_cookies', 'get_log', 'get_network_conditions',
          'get_screenshot_as_base64', 'get_screenshot_as_file', 'get_screenshot_as_png', 'get_window_position',
          'get_window_rect', 'get_window_size', 'maximize_window', 'minimize_window', 'implicitly_wait', 'quit',
          'refresh', 'save_screenshot', 'set_network_conditions', 'set_page_load_timeout', 'set_script_timeout',
          'set_window_position', 'set_window_rect', 'start_client', 'start_session', 'stop_client']]



def parse_explore_flights(text):
    selector = Selector(text=text)
    flights = selector.xpath('//div[contains(text(), "About these results")]/following-sibling::ol/li')
    data = []
    for flight in flights:
        destination = flight.xpath('.//h3/text()').get()
        date = flight.xpath('.//h3/following-sibling::div[1]/text()').get()
        stops = flight.xpath('.//h3/following-sibling::div[2]/span[1]/text()').get()
        price = flight.xpath('.//span[contains(@aria-label, "Brazilian reals")]/text()').get()
        if not price:
            continue
        price = float(price.replace('R$', '').replace(',', ''))
        data.append({
            "destination": destination,
            "price": price,
            "date": date,
            "stops": stops
        })
    data = sorted(data, key=lambda x: x['price'])
    return data


def parse_flights(text):
    selector = Selector(text=text)

    flights = selector.xpath('//h3[text()="Departing flights"]/following-sibling::ul/li')
    data = []
    for flight in flights:
        departure_time = flight.xpath('.//span[contains(@aria-label, "Departure time")]/text()').get()
        arrival_time = flight.xpath('.//span[contains(@aria-label, "Arrival time")]/text()').get()
        total_duration = flight.xpath('.//div[contains(@aria-label, "Total duration")]/text()').get()
        stops = flight.xpath('.//span[contains(@aria-label, "stops")]/text()').get() or flight.xpath('.//span[contains(@aria-label, "stop")]/text()').get()
        layovers = flight.xpath('.//div[contains(@aria-label, "Layover")]/@aria-label')
        layover = layovers[-1].get() if layovers else None
        price = flight.xpath('.//span[contains(@aria-label, "Brazilian reals")]/text()').get()
        operator = flight.xpath('.//span[contains(@aria-label, "Departure time")]/ancestor::div[1]/following-sibling::div[1]/span/text()').get()
        if not price:
            continue
        price = float(price.replace('R$', '').replace(',', ''))
        data.append({
            "departure_time": departure_time.replace("\u202f", " "),
            "arrival_time": arrival_time.replace("\u202f", " "),
            "total_duration": total_duration,
            "stops": stops,
            "layovers": layover,
            "price": price,
            "operator": operator
        })

    data = sorted(data, key=lambda x: x['price'])
    return data


@lru_cache()
def get_browser():
    return Browser(showWindow=False)


def get_flights(query="flights to GRU from CWB on 01-10-2024 through 25-10-2024 2 seats"):
    web = get_browser()
    query = quote(query)
    url = f"https://google.com/travel/flights?q={query}"
    logging.info(f"Going to {url}")
    web.go_to(url)
    logging.info("Waiting for page to load")
    web.click("Sort by")
    logging.info("Clicking on departure time")
    web.click("Departure time")
    logging.info("Clicking on more flights")
    web.click("more flights")

    sleep(10)
    html = web.get_page_source()
    logging.info("Parsing flights")
    return parse_flights(html)


def get_explore_flights(query="flights from CWB to anywhere, 2-week trip in the next 6 months 2 seats"):
    web = get_browser()
    query = quote(query)
    url = f"https://www.google.com/travel/explore?q={query}"
    logging.info(f"Going to {url}")
    web.go_to(url)

    sleep(5)
    html = web.get_page_source()
    logging.info("Parsing flights")
    return parse_explore_flights(html)


if __name__ == "__main__":
    while True:
        try:
            # flights = get_flights()
            flights = get_explore_flights()
            logging.info(len(flights))
            logging.info(flights)
        except Exception as e:
            logging.error(e)
        sleep(10)
