
from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.5/4/1.html'
stepic = 'https://stepik.org/lesson/732063/step/9?unit=733596'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)
    driver.get(url)

    for item in wait.until(ec.presence_of_all_elements_located(('class name', 'parent'))):
        source, target = item.find_elements('tag name', 'textarea')
        actions \
            .double_click(source) \
            .pause(0.5) \
            .drag_and_drop(source, target) \
            .perform()
        item.find_element('tag name', 'button').click()
    driver.find_element('id', 'checkAll').click()
    result = wait.until(ec.visibility_of_element_located(('id', 'congrats'))).text

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
