# не работает
# driver.execute_script("return window.innerWidth") = 610  driver.get_window_size() = {'width': 654, 'height': 404}
# driver.execute_script("return window.innerWidth") = 612  driver.get_window_size() = {'width': 655, 'height': 404}
# driver.execute_script("return window.innerWidth") = 612  driver.get_window_size() = {'width': 656, 'height': 404}
# driver.execute_script("return window.innerWidth") = 613  driver.get_window_size() = {'width': 657, 'height': 404}
# driver.execute_script("return window.innerWidth") = 614  driver.get_window_size() = {'width': 658, 'height': 404}
# driver.execute_script("return window.innerWidth") = 615  driver.get_window_size() = {'width': 659, 'height': 404}
# driver.execute_script("return window.innerWidth") = 617  driver.get_window_size() = {'width': 660, 'height': 404} !!!
# driver.execute_script("return window.innerWidth") = 617  driver.get_window_size() = {'width': 661, 'height': 404} !!!
# driver.execute_script("return window.innerWidth") = 618  driver.get_window_size() = {'width': 662, 'height': 404}
# driver.execute_script("return window.innerWidth") = 619  driver.get_window_size() = {'width': 663, 'height': 404}
# driver.execute_script("return window.innerWidth") = 620  driver.get_window_size() = {'width': 664, 'height': 404}
# driver.execute_script("return window.innerWidth") = 622  driver.get_window_size() = {'width': 665, 'height': 404}
# driver.execute_script("return window.innerWidth") = 622  driver.get_window_size() = {'width': 666, 'height': 404}
from time import sleep

from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://parsinger.ru/window_size/2/index.html'
stepic = 'https://stepik.org/lesson/732079/step/5?unit=733612'

env = Env()
env.read_env(recurse=False)

options = webdriver.ChromeOptions()
options.add_argument('--window-size=500,400')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 1)
    wait_stepic = WebDriverWait(driver, 15)

    driver.get(stepic)
    stepic = driver.current_window_handle
    driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
    driver.refresh()

    lst = [
        int(item.text) for item in
        wait_stepic.until(ec.presence_of_all_elements_located(('xpath', '//span[@class="hljs-number"]')))
    ]
    coords = list(zip(lst[:12], lst[12:]))
    print(*coords)

    driver.switch_to.new_window()
    driver.get(url)
    print((current_size := driver.get_window_size()))
    width = current_size.get('width')
    height = current_size.get('height')

    for coord in coords:
        x, y = coord
        print(x, y)

        while True:
            driver.set_window_size((width := width + 1), height)
            print(f'{driver.execute_script("return window.innerWidth") = }  {driver.get_window_size() = }')
            if driver.execute_script("return window.innerWidth") == x:
                break

        while True:
            driver.set_window_size(width, (height := height + 1))
            print(f'{driver.execute_script("return window.innerHeight") =}')
            if driver.execute_script("return window.innerHeight") == y:
                break

        result = wait.until(ec.visibility_of_element_located(('id', 'result'))).text
        print(width, height, result)
    sleep(100)

    driver.switch_to.window(stepic)
    wait_stepic.until(
        ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
    ).send_keys(result)
    wait_stepic.until(
        ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
    ).click()
    sleep(5)
