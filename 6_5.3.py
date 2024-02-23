from time import sleep

from environs import Env
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/infiniti_scroll_3/'
stepic = 'https://stepik.org/lesson/732069/step/4?unit=733602'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    action = ActionChains(driver)
    result = 0

    for item in range(1, 6):
        while True:
            action \
                .move_to_element(driver.find_element
                                 ('xpath', f'//*[@id="scroll-container_{item}"]/div')) \
                .scroll_by_amount(0, 1000) \
                .pause(1) \
                .perform()
            try:
                driver.find_element(
                    'xpath', f'//*[@id="scroll-container_{item}"]//*[@class="last-of-list"]'
                )
                break
            except NoSuchElementException:
                pass

        lst = driver.find_element('id', f'scroll-container_{item}').text
        result += sum(int(item) for item in lst.split())

    driver.switch_to.new_window()
    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    wait.until(
        ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
    ).send_keys(result)
    wait.until(
        ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
    ).click()
    sleep(5)
