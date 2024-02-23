from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.7/4/index.html'
stepic = 'https://stepik.org/lesson/732069/step/7?unit=733602'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')


with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    action = ActionChains(driver)
    last = None

    while True:
        lst = wait.until(ec.presence_of_all_elements_located(('xpath', '//*[@class="child_container"]')))
        if last == lst[-1]:
            break
        last = lst[-1]
        action.scroll_to_element(last).perform()

    for item in driver.find_elements('tag name', 'input'):
        if not int(item.get_attribute('value')) % 2:
            item.click()

    wait.until(ec.element_to_be_clickable(('tag name', 'button'))).click()

    alert = wait.until(ec.alert_is_present())
    result = alert.text
    alert.accept()

    driver.switch_to.new_window()
    driver.get(stepic)
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    wait.until(
        ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
    ).send_keys(result)
    wait.until(
        ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
    ).click()
    sleep(5)
