import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class BasicInstallTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("База українських кріейтерів", self.browser.title)

    def test_home_page_header(self):
        self.browser.get("http://localhost:8000")
        header_element = self.browser.find_element(By.TAG_NAME, "h1")
        header_text = header_element.text
        self.assertIn("База українських кріейтерів", header_text)


if __name__ == "__main__":
    unittest.main()
