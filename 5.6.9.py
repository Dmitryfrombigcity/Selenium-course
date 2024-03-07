from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.5/5/1.html'
stepic = 'https://stepik.org/lesson/732063/step/10?unit=733596'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)

    for item in wait.until(
            ec.presence_of_all_elements_located(
                ('xpath', '//span/..'))):

        color = item.find_element('xpath', 'span').text
        dropdown = Select(item.find_element('xpath', 'select'))
        options = dropdown.options
        dropdown.select_by_visible_text(color)

        for button in item.find_elements('xpath', 'div/button'):
            if button.get_attribute('data-hex') == color:
                button.click()
                break

        item.find_element('xpath', 'input[@type="checkbox"]').click()
        item.find_element('xpath', 'input[@type="text"]').send_keys(color)
        item.find_element('xpath', 'button').click()

    driver.find_element('xpath', '//button[text()="Проверить все элементы"]').click()
    alert = wait.until(ec.alert_is_present())
    result = alert.text
    alert.accept()

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
