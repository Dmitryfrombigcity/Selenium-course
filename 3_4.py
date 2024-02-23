from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/1/1.html'
stepic = 'https://stepik.org/lesson/731861/step/4?unit=733396'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    for item in driver.find_elements('xpath', '//input[@class="form"]'):
        item.send_keys('Текст')
    wait.until(ec.element_to_be_clickable(driver.find_element('id', 'btn'))).click()
    result = wait.until(ec.presence_of_element_located(('id', 'result'))).text
    driver.switch_to.new_window()
    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    wait.until(ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))).send_keys(result)
    wait.until(ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))).click()
    sleep(5)
