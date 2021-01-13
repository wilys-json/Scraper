from getpass import getpass
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from Scraper.config import Config
from Scraper.error import error
from Scraper.utils import _decode
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


    def _findObjects(self, element):
        """
        Generic function to find element in webpage.
        """
        obj = self._getObject(element)
        type, keyword = obj['type'], obj['keyword']
        inventory, attribute = obj['inventory'], obj['attribute']
        elements = self.find_elements(type, keyword)
        self.__dict__[inventory] = [element.get_attribute(attribute)
                                    for element in elements]


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


    def _scroll(self, element):
        obj = self._getObject(element)
        recursive = obj['recursive']

        if recursive:
            currentHeight = self.execute_script(
                             "return document.body.scrollHeight"
                             )
            while True:
                self.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                    )

                time.sleep(self.Wait)

                newHeight = driver.execute_script(
                            "return document.body.scrollHeight"
                            )
                if newHeight == currentHeight:
                    break
                currentHeight = newHeight
        else:
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
                )


    def scrapeObjects(self, element):
        obj = self._getObject(element)
        inventory = self.__dict__[obj['inventory']]
        action = obj['scrapeAction']
        for item in inventory:
            self.get(item)

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
        Generic login function. Implements 'loginSteps' in input API.
        """
        assert self.loginSteps, error.MISSING("login config")

        for stepElement in self.loginSteps:
            obj = self._getObject(stepElement)
            Scraper.__dict__[obj['action']](self, stepElement)
            sleep(self.Wait)


    def scrape(self):
        """
        Generic scrape function. Implements 'scrapeSteps' in input API.
        """
        assert self.scrapeSteps, error.MISSING("scrape config")

        for stepElement in self.scrapeSteps:
            obj = self._getObject(stepElement)
            Scraper.__dict__[obj['action']](self, stepElement)
            sleep(self.Wait)
