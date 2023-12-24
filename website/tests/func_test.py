from selenium import webdriver
import unittest


class BasicInstallTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_install(self):
        self.browser.get("http://localhost:8000/test")
        self.assertIn("Test Template", self.browser.title)


if __name__ == "__main__":
    unittest.main()
