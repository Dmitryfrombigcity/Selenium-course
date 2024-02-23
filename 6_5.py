from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/scroll/2/index.html'
stepic = 'https://stepik.org/lesson/732069/step/1?unit=733602'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    result = 0
    for item in wait.until(ec.presence_of_all_elements_located(('xpath', '//*[@class="item"]'))):
        item.find_element('tag name', 'input').click()
        if (temp := item.find_element('tag name', 'span').text) != '':
            result += int(temp)

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
