import functools

from selenium import webdriver


def getChromeBrowser(proxy: str = None, implicitWaitTime: int = 30,
                     incognito: bool=False, path: str=''):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('disable-infobars')

    if proxy:
        chromeOptions.add_argument(f'--proxy-server={proxy}')
    if incognito:
        chromeOptions.add_argument("--incognito")

    driver = webdriver.Chrome(executable_path=path,
                              chrome_options=chromeOptions)
    driver.implicitly_wait(implicitWaitTime)
    return driver


def browserHandler(proxy: str=None, implicitWaitTime: int = 30,
                   incognito: bool=False, path: str=''):
    def bhWrapper(func):
        @functools.wraps(func)
        def bh(*args, **kwargs):
            driver = getChromeBrowser(proxy, implicitWaitTime,
                                      incognito, path)
            try:
                func(driver, *args, **kwargs)
            finally:
                driver.quit()
        return bh
    return bhWrapper


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
