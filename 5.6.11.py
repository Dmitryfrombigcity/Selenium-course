from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/selenium/5.6/1/index.html'
stepic = 'https://stepik.org/lesson/732063/step/12?unit=733596'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with (webdriver.Chrome(options=options) as driver):
    wait = WebDriverWait(driver, 15)

    driver.get(stepic)
    stepic = driver.current_window_handle
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()
    wait.until(ec.presence_of_element_located(('xpath', '//details'))).click()
    lst = wait.until(ec.presence_of_all_elements_located(('xpath', '//details//span')))
    lst_txt = [item.text.strip("'") for item in lst]
    cookies = ({'name': name, 'value': value} for name, value in zip(lst_txt[1::4],
                                                                     lst_txt[3::4]))
    driver.switch_to.new_window()
    credentials = []
    driver.get(url)
    for cookie in cookies:
        driver.delete_all_cookies()
        driver.add_cookie(cookie)
        driver.refresh()
        wait.until(ec.title_is('Профиль'))

        credentials.append({
            'age': int(driver.find_element('id', 'age').text.split(':')[-1]),
            'skills': len(driver.find_element('id', 'skillsList').text.split()),
            'value': cookie['value']
        })

    for item in credentials:
        print(item)

    credentials.sort(key=lambda x: (x['age'], -x['skills']))
    desired_person = credentials[0]
    print('', desired_person, sep='\n')
    result = desired_person.get('value')

    driver.switch_to.window(stepic)
    wait.until(ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
               ).send_keys(result)
    wait.until(ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
               ).click()
    sleep(5)
