import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import traceback
from DataBase import *


HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 'accept': '*/*'}
info = []


def get_url(page=None):
    url = f'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118/f/tolko-v-nalichii=da?from=under_search&showCount=72&page={page}'
    return url


id_card = 0
def get_content(html):
    global id_card
    global info

    soup = BeautifulSoup(html, 'html.parser')

    info_cards = soup.find('div', class_='product-cards-layout product-cards-layout--list')
    info_cards = info_cards.find_all('div', class_='product-cards-layout__item ng-star-inserted')

    for card in info_cards:
        # 1 Picture
        picture = card.find('div', class_='product-card--list__picture')
        picture = picture.find('mvid-plp-product-picture')
        picture = picture.find_all('source')
        picture = f'http:{picture[0].get("srcset")}'

        # 2 Name
        name = card.find('div', class_='product-card--list__description')
        name = name.find('mvid-plp-product-title')
        name = name.get_text()

        # 3 Price
        price = card.find('mvid-plp-price-block')
        price = price.find('span')
        price = price.get_text()
        price = price.replace(' ', '').replace(' ', '')[:-1]

        # 4 Specifications
        specifics = ''
        all_specifics = card.find('mvid-plp-product-feature-list')
        list_name = all_specifics.find_all('span', class_='product-feature-list__name')
        list_value = all_specifics.find_all('span', class_='product-feature-list__value')

        value_id = 0
        for value in list_value:
            list_value[value_id] = value.get_text()
            value_id += 1

        list_value = list(filter(filter_empty, list_value))

        value_id = 0
        for value in list_value:
            if len(value) == 1:
                list_value[value_id:value_id+2] = [' '.join(
                    list_value[value_id:value_id+2])]
            value_id += 1

        for row in range(0, 5):
            specifics += f'{list_name[row].get_text()}: {list_value[row]}\n'

        # 5 Hrefs
        more = card.find('div', class_='product-card--list__description')
        more = more.find('mvid-plp-product-title')
        more = more.find('a', href=True)
        more = f"https://www.mvideo.ru{more.get('href')}"

        info.append({
            'id': int(id_card),
            'picture': picture,
            'name': name,
            'price': int(price),
            'specifications': specifics,
            'more': more
        })
        INSERT_NEW_LAPTOP(id_card, picture, name, price, specifics, more)

        id_card += 1

    print('Yes')


def parse():
    for page in range(1, 6):
        URL = get_url(page=page)

        html = get_html_with_driver(URL, page=page)
        if html != None:
            get_content(html)

    with open('info_laptops.json', 'w', encoding='utf-8') as file:
        json.dump(info, file, ensure_ascii=False)


def get_html_with_driver(url, page=None):
    chrome_options = Options()
    chrome_options.add_argument("window-size=1400,900")
    driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')

    html = None
    driver.get(url=url)
    time.sleep(5)

    '''list_switcher = driver.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/mvid-plp/mvid-product-list-block/mvid-product-list-controls/mvid-view-switcher/div')
    list_switcher.click()
    time.sleep(3)'''

    try:
        y = 1000
        for timer in range(0, 40):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 700
            time.sleep(1)

    except Exception as ex:
        print(traceback.format_exc())
        return None

    html = driver.page_source

    driver.close()
    driver.quit()

    return html


def filter_empty(text):
    if text != '':
        return True
    else:
        return False


parse()
