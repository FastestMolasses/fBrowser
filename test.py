import fBrowser

from time import sleep


@fBrowser.browserHandler()
def main(driver):
    driver.get('https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f')
    fBrowser.login(driver, email='testing@gmail.com', password='abc123')
    sleep(5)


main()
