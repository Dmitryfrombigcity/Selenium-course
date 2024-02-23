from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5/5.html'
stepic = 'https://stepik.org/lesson/731861/step/9?unit=733396'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with (webdriver.Chrome(options=options) as driver):
    wait = WebDriverWait(driver, 15)
    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    lst_num = wait.until(ec.presence_of_all_elements_located(('xpath', '//span[@class="hljs-number"]')))
    set_num = set(item.text for item in lst_num)

    driver.switch_to.new_window()
    driver.get(url)
    lst_check = wait.until(ec.presence_of_all_elements_located(('class name', 'check')))
    for item in lst_check:
        if item.get_attribute('value') in set_num:
            item.click()
    wait.until(ec.element_to_be_clickable(('class name', 'btn'))).click()
    result = wait.until(ec.visibility_of_element_located(('id', 'result'))).text
    driver.switch_to.window(driver.window_handles[0])

    wait.until(ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
               ).send_keys(result)
    wait.until(ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
               ).click()
    sleep(5)
