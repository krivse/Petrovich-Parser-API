import logging
import os

from typing import Optional

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
import requests


from errors import bad_request


def options_driver():
    """Configuration of web driver settings."""
    selenium_logger = logging.getLogger('selenium')

    selenium_logger.setLevel(logging.ERROR)

    # user_agent = UserAgent().chrome
    chrome_options = webdriver.ChromeOptions()
    # передача необходимых опций в браузер
    # открытие браузера в фоновом режиме эквивалентно chrome_options.headless = True
    chrome_options.add_argument("--headless")
    # отключение автоматизированного управления браузером
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # игнорирование незащищенного соединения
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--no-check-certificate')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.page_load_strategy = 'eager'

    # установка user-agent
    chrome_options.add_argument(
        f'--user-agent={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537"}')
    # отключаем webdriver
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    browser = webdriver.Chrome(
        service=Service(executable_path=f'{os.path.dirname(os.path.abspath(__file__))}/chromedriver'),
        options=chrome_options
    )

    return browser


def calculate_materials(type_room, length, width, height) -> Optional[list[dict]]:
    """Parser for counting materials depending on the type of room."""
    browser = options_driver()
    wait = WebDriverWait(browser, 5)

    # URL address
    petrovich = 'https://petrovich.ru/renovation/rooms-step/'

    data = {
        "type": type_room,
        "materials": []
    }
    try:
        browser.get(petrovich)

        if type_room in ['Кухня', 'Комната', 'Гостиная', 'Санузел']:
            # choice of room type
            search_room = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{type_room}')]"))
            )
            search_room.click()
        else:
            # click on the "Другое" button
            other_room = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Другое')]"))
            )
            other_room.click()
            # search and click on the button
            search_room_2 = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{type_room}')]"))
            )
            search_room_2.click()

        # add settings attributes
        length_value = wait.until(EC.visibility_of_element_located((By.NAME, 'length')))
        length_value.send_keys(length)
        width_value = wait.until(EC.visibility_of_element_located((By.NAME, 'width')))
        width_value.send_keys(width)
        height_value = wait.until(EC.visibility_of_element_located((By.NAME, 'height')))
        height_value.send_keys(height)

        # click on the "Продолжить" button
        continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Продолжить')]"))
        )
        continue_button.click()

        # search for a list of materials
        type_room_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[starts-with(@class, 'pt-accordion-tab-sm___')]"))
        )
        type_work_button = WebDriverWait(type_room_button, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Черновые')]"))
        )
        type_work_button.click()

        # opening of the card of goods
        frame_room = WebDriverWait(
            type_room_button, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'pt-accordion___MRiZn')))

        materials = WebDriverWait(type_room_button, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pt-accordion-tab-md___foXPg')))

        # data collection for floor
        WebDriverWait(frame_room, 5).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='pt-accordion-id-3']"))
        ).click()
        floor = materials[0]
        floor_material = WebDriverWait(floor, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pt-table-row___hKiUu'))
        )[1:]
        data_collection(floor_material, 'Пол', data)

        # data collection for floor walls
        id_4 = WebDriverWait(frame_room, 5).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='pt-accordion-id-4']"))
        )
        browser.execute_script('arguments[0].click()', id_4)
        walls = materials[1]
        walls_material = WebDriverWait(walls, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pt-table-row___hKiUu'))
        )[1:]
        data_collection(walls_material, 'Стены', data)

        # data collection for sealing
        id_5 = WebDriverWait(frame_room, 5).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='pt-accordion-id-5']"))
        )
        browser.execute_script('arguments[0].click()', id_5)
        ceiling = materials[2]
        ceiling_material = WebDriverWait(ceiling, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pt-table-row___hKiUu'))
        )[1:]
        data_collection(ceiling_material, 'Потолок', data)

        # collecting additional information about the goods
        collecting_additional_information(data, browser, wait)

        return [data]

    except TimeoutException:
        logging.error(f'TimeoutException. Время ожидания поиска элемента истекло!')
        bad_request('Время ожидания поиска элемента истекло!')
    except Exception as ex:
        logging.error(f'Exception. Message {ex}')
        bad_request('Ошибка при выполнении запроса!')
    finally:
        browser.close()
        browser.quit()


def data_collection(materials, part_room, items) -> None:
    """Data collection about the goods."""
    products = []
    for i in materials:
        data = WebDriverWait(i, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pt-table-cell___umhSz'))
        )
        img = WebDriverWait(data[0], 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        ).get_attribute('src')
        url = WebDriverWait(data[0], 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pt-link___JRuYu'))
        ).get_attribute('href')
        title = WebDriverWait(data[0], 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        ).get_attribute('alt')
        article = WebDriverWait(data[0], 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pt-typography____JqPt'))
        )
        price = WebDriverWait(data[2], 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'p'))
        )
        amount = WebDriverWait(data[3], 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'span'))
        )
        summ = WebDriverWait(data[4], 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'p'))
        )
        format_price = price.text.replace('\u2009₽', '')
        format_summ = summ.text.replace('\u2009₽', '').replace(' ', '')
        products.append(
            {
                'article': article.text,
                'name': title,
                'amount': amount.text,
                'price': format_price,
                'summ': format_summ,
                'logo': img,
                'url': url
            }
        )
    items.get('materials').append(
        {
            'name': part_room,
            'type': 'Черновые',
            'products': products
        }
    )


def collecting_additional_information(items, browsers, wait) -> None:
    """Collecting additional information about the goods."""
    materials = items.get('materials')

    for item in range(len(materials)):
        products = items.get('materials')[item].get('products')
        for i in range(len(products)):
            url = products[i].get('url')
            page_of_good = requests.get(url)
            soup = BeautifulSoup(page_of_good.text, 'lxml')

            description = soup.find('div', class_='product-body').find('p', class_='product-description-text').text
            characteristic = soup.find('ul', class_='product-properties-list')
            title = characteristic.find_all('li', class_='data-item')[1]
            brand = characteristic.find_all('li', class_='data-item')[2]
            img = soup.find('img', attrs='swiper-lazy').get('srcset').split(', ')[1].replace(' 2x', '')

            products[i]['description'] = description
            for t in title:
                if t.text != 'Тип товара':
                    products[i]['type'] = t.text
            for b in brand:
                if b.text != 'Бренд' and 'Бренд' in brand:
                    products[i]['brand'] = b.text
                elif 'Бренд' not in brand:
                    products[i]['brand'] = ''
            products[i]['img'] = img

            # browsers.get(url)

            # try:
            #     WebDriverWait(browsers, 1).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, 'show-more-description'))
            #     ).click()
            # except TimeoutException:
            #     pass
            # description = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-description-text')))
            # technology_title = wait.until(
            #     EC.visibility_of_element_located((By.CLASS_NAME, 'product-description-title')))
            # technology_structure_list = wait.until(
            #     EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product-description-list')))
            #
            # technology = [technology_title.text]
            # structure = []
            # for j in range(len(technology_structure_list)):
            #     description_el = WebDriverWait(technology_structure_list[j], 30).until(
            #         EC.presence_of_all_elements_located((By.TAG_NAME, 'li'))
            #     )
            #     for el in description_el:
            #         if j == 0:
            #             if el.text != '':
            #                 technology.append(el.text)
            #         else:
            #             structure.append(el.text.strip(';'))

            # characteristic = wait.until(
            #     EC.visibility_of_element_located((By.CLASS_NAME, 'product-properties-list')))
            # title = WebDriverWait(characteristic, 5).until(
            #     EC.visibility_of_all_elements_located((By.CLASS_NAME, 'pt-link___JRuYu')))
            # img = wait.until(
            #     EC.presence_of_element_located((By.XPATH, "//div[@class='content-slide']/img"))
            # ).get_attribute('srcset')
            #
            # format_img = img.replace(' 1x', '').replace(' 2x', '')
            # products[i]['img'] = format_img
            # products[i]['type'] = title[0].text
            # if len(title) > 1:
            #     products[i]['brand'] = title[1].text
            # else:
            #     products[i]['brand'] = ''
            # products[i]['description'] = description.text
            # products[i]['technology'] = technology
            # products[i]['structure'] = structure
