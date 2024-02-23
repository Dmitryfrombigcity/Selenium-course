from time import sleep

from environs import Env
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.8/5/index.html'
stepic = 'https://stepik.org/lesson/732079/step/9?unit=733612'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15, poll_frequency=0.1)
    driver.get(url)

    for iframe in driver.find_elements('tag name', 'iframe'):
        driver.switch_to.frame(iframe)
        wait.until(ec.element_to_be_clickable(('tag name', 'button'))).click()
        number = wait.until(ec.presence_of_element_located(('id', 'numberDisplay'))).text
        driver.switch_to.default_content()
        wait.until(ec.visibility_of(driver.find_element('id', 'guessInput'))).clear()
        driver.find_element('id', 'guessInput').send_keys(number)
        wait.until(ec.element_to_be_clickable(('id', 'checkBtn'))).click()
        try:
            if alert := WebDriverWait(driver, 1).until(ec.alert_is_present()):
                result = alert.text
                alert.accept()
                break
        except TimeoutException:
            continue

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
