###################################################################################
# The MIT License (MIT)                                                           #
#                                                                                 #
# Copyright (c) 2021 Wilson Lam                                                   #
#                                                                                 #
# Permission is hereby granted, free of charge, to any person obtaining a copy of #
# this software and associated documentation files (the "Software"), to deal in   #
# the Software without restriction, including without limitation the rights to    #
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of#
# the Software, and to permit persons to whom the Software is furnished to do so, #
# subject to the following conditions:                                            #
#                                                                                 #
# The above copyright notice and this permission notice shall be included in all  #
# copies or substantial portions of the Software.                                 #
#                                                                                 #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS#
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR  #
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER  #
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN         #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.      #
###################################################################################

import os
import shutil
import requests
from getpass import getpass
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from Scraper.config import Config
from Scraper.error import error
from Scraper.utils import _decode
from time import sleep
from datetime import datetime


# Generic features to handle file downloading
DOWNLOAD_CONFIG = {
    "downloadCounts",  # Counter of files for file naming (int)
    "downloadBuffer",  # String to store target Url to download (str)
    "downloadDirectory",  # target download directory (str)
    "downloadFileFormat"  # target file format (str)
    }


class Scraper(Chrome, Config):
    """
    Generic class for scraping.
    Parents: selenium.webdriver.Chrome, Scraper.config.Config
    """
    def __init__(self, params):
        """
        Instantiates Scraper object.
        @param params  (dict) : dictionary (JSON) object for Config
        """
        Chrome.__init__(self,
                        ChromeDriverManager().install())
        Config.__init__(self, **params)
        # Create timestamp
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


    def _getObject(self, element, *args, **kwargs):
        """
        Get object (element) defined in script JSON file.
        @param element  (str) : name of element

        return:
        Respective element defined in JSON script (dict)
        """
        assert element in self.__dict__, error.INVALID(element)

        return self.__dict__[element]


    def _findObjects(self, element, *args, **kwargs):
        """
        Generic function to find elements in webpage.
        @param element  (str) : name of element

        Stores found elements in defined `invetory` attribute of instance as a
        list.
        """
        # Get defined object
        obj = self._getObject(element)

        # Get defined parameters
        # `type` : type of web element
        # `keyword` : keyword to search
        # `inventory` : instance attribute to which results will be stored
        # `attribute` : web element attribute
        type, keyword = obj['type'], obj['keyword']
        inventory, attribute = obj['inventory'], obj['attribute']

        # Buffer
        sleep(self.Wait)

        # Find element in webpage
        elements = self.find_elements(type, keyword)

        # Get webpage attribute if defined; stores results in instance attrib.
        if attribute:
            self.__dict__[inventory] = [element.get_attribute(attribute)
                                        for element in elements]
        else:
            self.__dict__[inventory] = elements


    def _findObject(self, element, *args, **kwargs):
        """
        Generic function to find an element in webpage.
        @param element  (str) : name of element

        Stores found element in defined `invetory` attribute of instance.
        """
        # Get defined object
        obj = self._getObject(element)

        # Get defined parameters
        # `type` : type of web element
        # `keyword` : keyword to search
        # `inventory` : instance attribute to which result will be stored
        # `attribute` : web element attribute
        type, keyword = obj['type'], obj['keyword']
        inventory, attribute = obj['inventory'], obj['attribute']

        # Buffer
        sleep(self.Wait)

        # Find element
        attempts = 0
        while attempts < self.Patience:
            try:
                element = self.find_element(type, keyword)
                break
            except:
                sleep(self.LongWait)
                attempts += 1

        # Get webpage attribute if defined; stores result in instance attrib.
        if attribute:
            self.__dict__[inventory] = element.get_attribute(attribute)
        else:
            self.__dict__[inventory] = element


    def _click(self, element, *args, **kwargs):
        """
        Generic click function.
        @param element  (str) : name of element

        Perform click on found element.
        """
        # Get defined object
        obj = self._getObject(element)

        # Get defined parameters
        # `type` : type of web element
        # `keyword` : keyword to search
        type, keyword = obj['type'], obj['keyword']

        # Perform click; skip if Error / Exception raised
        try:
            self.find_element(type, keyword).click()
        except:
            pass


    def _fillContent(self, element, *args, **kwargs):
        """
        Generic function to fill in content.
        @param element  (str) : name of element

        Fill content in webpage.
        """
        # Get defined object
        obj = self._getObject(element)

        # Make sure `encoded` parameter is defined
        assert 'encoded' in obj, error.MISSING('encoded')

        encoded = obj['encoded']

        try:
            if encoded:  # Decode the object if string has been encoded
                reverse = obj['reverse']
                content = _decode(secret_string=obj['content'], reverse=reverse)
            else:  # Otherwise, get plain text
                content = obj['content']
        except KeyError:  # Prompt for input if `content` not found
            content = input("Please enter {}:".format(obj['keyword']))

        try:
            type, keyword = obj['type'], obj['keyword']
            self.find_element(type, keyword).clear()  # Clear content
            self.find_element(type, keyword).send_keys(content)  # Fill content
        except:
            pass


    def _tryClicks(self, element, *args, **kwargs):
        """
        Try out elements to click until success or end of tryout list.
        Uses when user not sure if website has changed web element.
        @param element  (str) : name of element

        Find & click the first clickable element defined in the tryout list.
        """
        try:
            # Get defined object & parameters
            obj = self._getObject(element)
            type, keyword = obj['type'], obj['keyword']
        except:
            print(error.MISSING(['type', 'keyword']))

        # Make sure tryouts is a list
        assert isinstance(keyword, list), "Tryouts must be an array."

        # Try clicking until an element is clickable
        for item in keyword:
            try:
                self.find_element(type, item).click()
                break
            except:
                sleep(self.Wait)  # Buffer
                continue


    def _scrollDown(self, element, *args, **kwargs):
        """
        Generic scrolling down function.
        @param element  (str) : name of element

        Scroll down the webpage.
        """
        # Get defined object
        obj = self._getObject(element)
        # Get `recursive` parameter
        recursive = obj['recursive']

        # If `recursive` is `True`, scroll until end is reached
        if recursive:
            # Track Pre-scroll Height
            currentHeight = self.execute_script(
                             "return document.body.scrollHeight"
                             )
            while True:
                # Scroll
                self.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                    )
                # Buffer
                sleep(self.LongWait)
                # Track new Height
                newHeight = self.execute_script(
                            "return document.body.scrollHeight"
                            )
                # End of page is reached
                if newHeight == currentHeight:
                    break
                # Update height
                currentHeight = newHeight

        else:  # Perform a single scroll
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
                )


    def _downloadObject(self, *args, **kwargs):
        """
        Function to download object from `downloadBuffer` attr of instance.
        """
        # Make sure all `DOWNLOAD_CONFIG` params are defined in JSON Script
        assert DOWNLOAD_CONFIG.intersection(self.__dict__),\
        error.MISSING("download config")

        # Create directory if not exist
        if not os.path.exists(self.downloadDirectory):
            os.mkdir(self.downloadDirectory)

        # File path strings
        directory = "{}".format(self.downloadDirectory)
        filename = "{}_{:04d}{}".format(self.timestamp,
                                        self.downloadCounts,
                                        self.downloadFileFormat)

        # Write stream to file
        with open(os.path.join(directory, filename), "wb") as outputFile:
            response = requests.get(self.__dict__[self.downloadBuffer],
                                    stream=True)
            shutil.copyfileobj(response.raw, outputFile)

        self.downloadCounts += 1  # Increment file index


    def _scrapeFromUrl(self, element, *args, **kwargs):
        """
        Implement actions of scraping from webpage URLs.
        @param element  (str) : name of element

        Implement actions stored in `scrapeActions`
        """
        # Get defined object
        obj = self._getObject(element)

        # Get lists of URLs to scrape
        URLs = self.__dict__[obj['inventory']]
        # Get list of actions to implement
        actions = obj['scrapeActions']
        # Iterate over URLs
        for URL in URLs:
            self.get(URL)
            for action in actions:
                actionObj = self._getObject(action)
                # Call Scraper methods
                Scraper.__dict__[actionObj['action']](self, action)


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

        # Call methods defined in `loginSteps` of JSON script
        for stepElement in self.loginSteps:
            obj = self._getObject(stepElement)
            # Call Scraper methods
            Scraper.__dict__[obj['action']](self, stepElement)
            sleep(self.Wait)


    def scrape(self):
        """
        Generic scrape function. Implements 'scrapeSteps' in input API.
        """
        assert self.scrapeSteps, error.MISSING("scrape config")

        # Call methods defined in `scrapeSteps` of JSON script
        for stepElement in self.scrapeSteps:
            obj = self._getObject(stepElement)
            Scraper.__dict__[obj['action']](self, stepElement)
            sleep(self.Wait)
