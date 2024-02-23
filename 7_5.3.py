from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/window_size/1/'
stepic = 'https://stepik.org/lesson/732079/step/4?thread=solutions&unit=733612'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=500,500')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)

    print((current_size := driver.get_window_size()))
    width = current_size.get('width')
    height = current_size.get('height')

    while True:
        driver.set_window_size((width := width + 1), height)
        if driver.execute_script("return window.innerWidth") == 555:
            break

    while True:
        driver.set_window_size(width, (height := height + 1))
        if driver.execute_script("return window.innerHeight") == 555:
            break

    print(width, height)
    result = wait.until(ec.presence_of_element_located(('id', 'result'))).text

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
