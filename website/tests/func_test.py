from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest


class BasicInstallTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_install(self):
        self.browser.get("http://localhost:8000/test")
        self.assertIn("Test Template", self.browser.title)


if __name__ == "__main__":
    unittest.main()
