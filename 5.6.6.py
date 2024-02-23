from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/scroll/4/index.html'
stepic = 'https://stepik.org/lesson/732063/step/7?unit=733596'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)
    result = 0
    driver.get(url)

    for item in wait.until(ec.presence_of_all_elements_located(('class name', 'btn'))):
        current_result = driver.find_element('id', 'result').text
        driver.execute_script('arguments[0].scrollIntoView(true);', item)
        item.click()

        for _ in range(100):  # if current and previous results are equal -> 10 sec limit
            if (temp := driver.find_element('id', 'result').text) != current_result:
                break
            sleep(0.1)
        result += int(temp)

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
