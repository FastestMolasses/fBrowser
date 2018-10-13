import functools

from time import sleep
from typing import Union
from random import uniform
from selenium import webdriver
# TODO: FIREFOX
# TODO: TAB / CONTEXT MANAGER


def getChromeBrowser(proxy: str = None, implicitWaitTime: int = 30,
                     incognito: bool=False, headless: bool=False) -> webdriver.Chrome:
    """
        Returns an instance of the webdriver for Chrome.

        :param proxy: Proxy to connect to - '<host>:<port>\n
        :param implicitWaitTime: Implicit wait time for the browser\n
        :param incognito: Whether to open in incognito or not\n
        :param headless: Run the browser in headless mode
    """
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')

    if proxy:
        chromeOptions.add_argument(f'--proxy-server={proxy}')
    if incognito:
        chromeOptions.add_argument("--incognito")
    if headless:
        chromeOptions.add_argument('--headless')

    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.implicitly_wait(implicitWaitTime)
    return driver


def browserHandler(proxy: str=None, implicitWaitTime: int = 30,
                   incognito: bool = False, headless: bool=False):
    """
        Creates and handles the browser driver. Will automatically close
        if an exception occurs or when the program ends.

        :param proxy: Proxy to connect to - '<host>:<port>\n
        :param implicitWaitTime: Implicit wait time for the browser\n
        :param incognito: Whether to open in incognito or not\n
        :param headless: Run the browser in headless mode
    """
    def bhWrapper(func):
        @functools.wraps(func)
        def bh(*args, **kwargs):
            driver = getChromeBrowser(proxy, implicitWaitTime,
                                      incognito, headless)
            try:
                func(driver, *args, **kwargs)
            finally:
                driver.quit()
        return bh
    return bhWrapper


def fillInputs(driver: webdriver.Chrome, inputXpaths: list = [],
               values: Union[str, list]=[]) -> None:
    """
        Fills a list of inputs with the specified value(s). If a list
        is passed, then the inputs will be filled with each value respectively.
        If the lists do not have equal lengths, then the amount of inputs filled will
        be the smallest length between the lists. If a string is passed, then all the 
        inputs will be filled with that value.

        :param driver: The instance of the web driver\n
        :param inputXpaths: A list of xpaths pointing to the input elements\n
        :param values: A string or list to fill the input elements with
    """
    inputs = [driver.find_element_by_xpath(i) for i in inputXpaths]

    if isinstance(values, str):
        for i in inputs:
            i.send_keys(values)

    elif isinstance(values, list):
        for i, j in zip(inputs, values):
            i.send_keys(j)


def login(driver: webdriver.Chrome, email: str = '',
          username: str = '', password: str = '',
          oneAtTime: bool=False, humanType: bool=False) -> None:
    """
        Will attempt to login to the current page. It will find elements
        that have the 'type' attribute associating it with an email, username,
        or password. If the password input only appears after you enter your
        email/username, make sure that `onAtTime` is set to True.

        :param driver: The instance of the web driver\n
        :param email: The email to sign in with\n
        :param username: The username to sign in with\n
        :param password: The password for the login\n
        :param oneAtTime: Bool indicating that an enter key needs to be pressed
        between each input\n
        :param humanType: Type at a human speed
    """
    # TODO: CHECK IF ELEMENTS EXIST FIRST, IF NOT THROW ERROR
    if email:
        email = email + '\n' if oneAtTime else email
        x = driver.find_element_by_xpath('//*[@type="email"]')

        if humanType:
            humanType(driver, x, email)
        else:
            x.send_keys(email)

    if username:
        username = username + '\n' if oneAtTime else username
        x = driver.find_element_by_xpath('//*[@type="username"]')

        if humanType:
            humanType(driver, x, username)
        else:
            x.send_keys(username)

    sleep(1)
    if password:
        x = driver.find_element_by_xpath('//*[@type="password"]')
        if humanType:
            humanType(driver, x, password)
        else:
            x.send_keys(password + '\n')


def humanType(driver: webdriver.Chrome,
              element: webdriver.remote.webelement,
              value: str) -> None:
    """
        Fills an input with a human typing speed. Useful if you
        don't want to get flagged as a bot.

        :param driver: The instance of the web driver\n
        :param element: The input element to fill
        :param value: What to fill the input with
    """
    for i in value:
        element.send_keys(i)
        # Sleep a random amount between each key press
        sleep(uniform(0.05, 0.10))


def newTab(func):
    """
        Runs the function in a new tab, then closes and 
        switches back context once it finishes.
    """
    @functools.wraps(func)
    def nt(driver, *args, **kwargs):
        driver.execute_script("window.open('', '_blank')")
        oldWindow = driver.current_window_handle
        driver.switch_to_window(driver.window_handles[-1])

        func(driver, *args, **kwargs)
        driver.close()
        driver.switch_to_window(oldWindow)
    return nt
