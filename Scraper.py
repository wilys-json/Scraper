from getpass import getpass
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from Config import Config
from error import error
from utils import _decode
from time import sleep

class Scraper(Chrome, Config):
    """
    Generic class for scraping.
    """
    def __init__(self, params):
        Chrome.__init__(self, ChromeDriverManager().install())
        Config.__init__(self, **params)


    def _getObject(self, element):
        """
        Get object from JSON.
        """
        assert element in self.__dict__, error.INVALID(element)

        return self.__dict__[element]


    def _click(self, element):
        """
        Generic click function
        """
        obj = self._getObject(element)
        type, keyword = obj['type'], obj['keyword']
        self.find_element(type, keyword).click()


    def _fillContent(self, element):
        """
        Generic function to fill in content
        """
        obj = self._getObject(element)

        assert 'encoded' in obj, error.MISSING('encoded')

        encoded = obj['encoded']

        try:
            if encoded:
                reverse = obj['reverse']
                content = _decode(secret_string=obj['content'], reverse=reverse)
            else:
                content = obj['content']
        except KeyError:
            content = input("Please enter {}:".format(obj['keyword']))

        try:
            type, keyword = obj['type'], obj['keyword']
            self.find_element(type, keyword).clear()
            self.find_element(type, keyword).send_keys(content)
        except:
            pass


    def _tryClicks(self, element):
        """
        Try out elements to click until success or end of tryout list.
        """
        try:
            obj = self._getObject(element)
            type, keyword = obj['type'], obj['keyword']
        except:
            print(error.MISSING(['type', 'keyword']))

        assert isinstance(keyword, list), "Tryouts must be an array."

        attempts = 0
        while attempts < len(keyword):
            try:
                self.find_element(type, keyword[attempts]).click()
                break
            except:
                attempts += 1
                sleep(self.Wait)


    def gotoBaseUrl(self):
        """
        Go to Base page.
        """
        try:
            self.get(self.BaseUrl)
        except:
            self.BaseUrl = input("Please enter base url:")

    def gotoTargetUrl(self):
        """
        Go to Target page.
        """
        try:
            self.get(self.TargetUrl)
        except:
            self.TargetUrl = input("Please enter target url:")

    def login(self):
        """
        Generic login function.
        """
        assert self.loginSteps, error.MISSING("login config")

        for stepElement in self.loginSteps:
            obj = self._getObject(stepElement)
            Scraper.__dict__[obj['action']](self, stepElement)
            sleep(self.Wait)
