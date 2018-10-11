import functools

from time import sleep
from typing import Union
from random import uniform
from selenium import webdriver


def getChromeBrowser(proxy: str = None, implicitWaitTime: int = 30,
                     incognito: bool=False):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')

    if proxy:
        chromeOptions.add_argument(f'--proxy-server={proxy}')
    if incognito:
        chromeOptions.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.implicitly_wait(implicitWaitTime)
    return driver


def browserHandler(proxy: str=None, implicitWaitTime: int = 30,
                   incognito: bool=False):
    def bhWrapper(func):
        @functools.wraps(func)
        def bh(*args, **kwargs):
            driver = getChromeBrowser(proxy, implicitWaitTime,
                                      incognito)
            try:
                func(driver, *args, **kwargs)
            finally:
                driver.quit()
        return bh
    return bhWrapper


def fillInputs(driver: webdriver.Chrome, inputXpaths: list = [],
               values: Union[str, list]=[]):
    inputs = [driver.find_element_by_xpath(i) for i in inputXpaths]

    if isinstance(values, str):
        for i in inputs:
            i.send_keys(values)

    elif isinstance(values, list):
        for i, j in zip(inputs, values):
            i.send_keys(j)


def login(driver: webdriver.Chrome, email: str = '',
          username: str = '', password: str = ''):
    # TODO: CHECK IF ELEMENTS EXIST FIRST, IF NOT THROW ERROR

    if email:
        driver.find_element_by_xpath('//*[@type="email"]').send_keys(email)
    elif username:
        driver.find_element_by_xpath(
            '//*[@type="username"]').send_keys(username)

    if password:
        driver.find_element_by_xpath(
            '//*[@type="password"]').send_keys(password + '\n')


def humanType(driver: webdriver.Chrome,
              element: webdriver.remote.webelement,
              value: str):
    for i in value:
        element.send_keys(i)
        # Sleep a random amount between each key press
        sleep(uniform(0.05, 0.10))


def newTab(func):
    @functools.wraps(func)
    def nt(driver, *args, **kwargs):
        driver.execute_script("window.open('', '_blank')")
        oldWindow = driver.current_window_handle
        driver.switch_to_window(driver.window_handles[-1])

        func(driver, *args, **kwargs)
        driver.close()
        driver.switch_to_window(oldWindow)
    return nt
