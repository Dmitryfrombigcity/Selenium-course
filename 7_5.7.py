from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

stepic = 'https://stepik.org/lesson/732079/step/8?unit=733612'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    result = 0

    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    stepic = driver.current_window_handle
    items = wait.until(ec.presence_of_all_elements_located(('class name', 'hljs-string')))
    sites = [item.text.strip("'") for item in items]

    driver.switch_to.new_window()
    for site in sites:
        driver.get(site)
        wait.until(ec.element_to_be_clickable(('class name', 'check_box'))).click()
        result += (int(wait.until(ec.presence_of_element_located(('id', 'result'))).text)) ** 0.5

    driver.switch_to.window(stepic)
    wait.until(
        ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
    ).send_keys(round(result, 9))
    wait.until(
        ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
    ).click()
    sleep(5)
