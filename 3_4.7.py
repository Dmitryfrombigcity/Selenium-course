from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/6/6.html'
stepic = 'https://stepik.org/lesson/731861/step/11?unit=733396'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with (webdriver.Chrome(options=options) as driver):
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    dropdown = Select(
        wait.until(ec.presence_of_element_located(('id', 'selectId')))
    )
    dropdown.select_by_visible_text(
        str(
            eval(
                wait.until(ec.presence_of_element_located(('id', 'text_box'))).text
            )
        )
    )
    wait.until(ec.element_to_be_clickable(('id', 'sendbutton'))).click()
    result = wait.until(ec.visibility_of_element_located(('id', 'result'))).text

    driver.switch_to.new_window()
    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    wait.until(ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
               ).send_keys(result)
    wait.until(ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
               ).click()
    sleep(5)
