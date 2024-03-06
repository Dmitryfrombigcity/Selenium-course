from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.10/6/index.html'
stepic = 'https://stepik.org/lesson/897512/step/13?unit=1066949'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)
    driver.get(url)

    for slider in wait.until(
            ec.presence_of_all_elements_located(('xpath', '//div[@class = "slider-container"]'))
    ):
        x = slider.size.get('width')
        y = slider.size.get('height')
        value_target = int(slider.text.split()[-1])

        actions.click() \
            .drag_and_drop_by_offset(slider, -0.5 * x, y) \
            .perform()

        while int(slider.text.split()[0]) - value_target:
            slider.find_element('xpath', './input').send_keys("\ue014")

    result = wait.until(
        ec.visibility_of_element_located(('id', 'message'))
    ).text

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
