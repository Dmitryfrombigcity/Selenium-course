from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.9/3/index.html'
stepic = 'https://stepik.org/lesson/732083/step/5?unit=733616'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)

    driver.get(stepic)
    stepic = driver.current_window_handle
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    lst = [item.text.strip("'") for item in wait.until(
        ec.presence_of_all_elements_located(('class name', 'hljs-string')))
           ]
    print(lst)
    sleep(100)

    # driver.switch_to.new_window()
    # driver.get(stepic)
    # driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    # driver.refresh()
    # wait.until(
    #     ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
    # ).send_keys(result)
    # wait.until(
    #     ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
    # ).click()
    # sleep(5)
