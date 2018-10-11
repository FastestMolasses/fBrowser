# fBrowser | Quick-start Your Selenium Project
This library was created in order to help users quick-start their webscraping project. It includes several useful functions including a browser handler, new tab functionality, and more.

## Installation
```
$ pip3 install fBrowser
```

## Usage

### Browser Handler
You can decorate your function with a browserHandler. This will create the driver and properly quit it if an exception occurs or when the program ends.

```python
import fBrowser
from time import sleep


@fBrowser.browserHandler()
def main(driver):
    driver.get('https://www.google.com')
    sleep(5)


main()
```

### New Tab
Run a function in a new tab of Chrome. It will automatically close and switch contexts when it finishes executing.

```python
import fBrowser
from time import sleep


def loadTheVerge(driver):
    driver.get('https://www.theverge.com')


@fBrowser.browserHandler()
def main(driver):
    driver.get('https://www.google.com')
    sleep(2)
    fBrowser.newTab(loadTheVerge)(driver)
    sleep(2)


main()
```

### Login
Use this helper function to login into a site. Simply pass in your email / username and your password. (This function assumes that the input tags in the form have attributes @type=username, @type=email, or @type=password).

```python
import fBrowser


@fBrowser.browserHandler()
def main(driver):
    driver.get(
        'https://stackoverflow.com/users/login')
    fBrowser.login(driver, email='testing@gmail.com', password='abc123')


main()
```

### Fill Inputs
Quickly fill multiple inputs with either a single value or multiple values.

```python
import fBrowser


@fBrowser.browserHandler()
def main(driver):
    driver.get('example.com')
    # A list of xpaths to the inputs
    xpaths = ['//*[@name="foo"]', '//*[@name="bar"]', '//@name="fooBar"']

    # Fill with multiple values
    fBrowser.fillInputs(driver, xpaths, ['value1', 'value2', 'value3'])

    # Or pass in one value
    fBrowser.fillInputs(driver, xpaths, 'hello world')


main()
```

### Human Type
Don't want to get flagged as a bot? Fill your inputs using a human-like typing speed.

```python
import fBrowser
from time import sleep


@fBrowser.browserHandler()
def main(driver):
    driver.get('https://www.google.com')
    chatInput = driver.find_element_by_xpath('//*[@name="q"]')
    # Will input the string at a human-like typing speed
    fBrowser.humanType(driver, chatInput, 'Hello world!')
    sleep(5)


main()
```

## Contributing

1. Fork it (<https://github.com/FastestMolasses/fBrowser/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Donate

If you're feeling grateful and want to support future development, feel free to donate 😁

---

**BTC**: 3HZ5zJ4sDEfMgTsN3YXA2BhYZTEfiUhpsq

**ETH**: 0x0D93Fc09CCfCADC099A24712AF090C30c287743D

**LTC**: MJRZbebzeJF8DUoFtJvpqQNfh1UnNmMVe1
