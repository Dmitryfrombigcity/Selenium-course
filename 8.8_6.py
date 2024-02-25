from time import sleep
from typing import Callable, Literal, Any

from environs import Env
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.9/5/index.html'
stepic = 'https://stepik.org/lesson/732083/step/7?unit=733616'


def text_to_be_changed_in_element(
        element: WebElement,
        text_: str = ''
) -> Callable[[Any], str | Literal[False]]:
    def _predicate(_: Any) -> str | Literal[False]:
        try:
            if text_ != element.text:
                return element.text
            return False
        except StaleElementReferenceException:
            return False

    return _predicate


env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 30)
    driver.get(url)
    boxes = wait.until(ec.presence_of_all_elements_located(('class name', 'box_button')))
    code = []
    for box in boxes:
        box.click()
        wait.until(ec.visibility_of_element_located(('id', 'ad_window')))
        driver.find_element('id', 'close_ad').click()
        code.append(wait.until(text_to_be_changed_in_element(box)))
    result = '-'.join(code)

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
