import unittest
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_driver(browser):
    if (browser == 'chrome'):
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1200x768')
        capabilities = DesiredCapabilities.CHROME.copy()
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=capabilities,
            options=options
        )

        return driver

    if (browser == 'firefox'):
        options = webdriver.FirefoxOptions()
        options.add_argument('-width=1920')
        options.add_argument('-height=1080')
        options.set_preference("geo.prompt.testing", True)
        options.set_preference("geo.prompt.testing.allow", False)
        capabilities = DesiredCapabilities.FIREFOX.copy()

        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=capabilities,
            options=options
        )

        return driver

    raise ValueError('Browser not supported')


class BaseTestCase(unittest.TestCase):
    def __init__(self, testname, config, environment, browser):
        super(BaseTestCase, self).__init__(testname)
        BaseTestCase.environment = environment
        BaseTestCase.config = config[environment]
        BaseTestCase.browser = browser

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver(cls.browser)
        cls.driver.get(cls.config['url'])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def takeScreenshot(self, test_name):
        print(self.__class__.__name__)

    #     self.driver.get_screenshot_as_file();

    def generateExceptionReport(self, exception):
        driver = self.driver
        screenshot = driver.get_screenshot_as_base64()
        console_log = driver.get_log('browser')
        console_log_string = json.dumps(console_log)
        formatedException = '''
        <p class="lead">{0}</p>
        
        <h4>Browser Screenshot</h4>
        <img src="data:image/png;base64,{1}">
        
        <h5>Browser Console</h5>
        <code>{2}</code>
        '''.format(exception, screenshot, console_log_string)

        return formatedException
