import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    def test_pagination_with_category_selection(self):
        self.browser.get("http://localhost:8000")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button.btn.btn-primary[type="submit"]')))

        checkboxes = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.NAME, 'categories'))
        )

        checkboxes = self.browser.find_elements(By.NAME, 'categories')
        for checkbox in checkboxes[:5]:
            checkbox.click()

        search_button = self.browser.find_element(By.CSS_SELECTOR,
                                                  'button.btn.btn-primary[type="submit"]')

        search_button.submit()
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Next"]')))
        try:
            next_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
            last_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Last"]')
        except NoSuchElementException:
            print("Paginator error in the First page.")

        next_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="First"]')))
        assert self.browser.current_url == "http://localhost:8000/youtuber_list/?page=2"
        try:
            first_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="First"]')
            last_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Last"]')
            previous_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Previous"]')
            next_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
        except NoSuchElementException:
            print("Paginator error in the second page.")

        last_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="First"]')))
        try:
            first_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="First"]')
            previous_button = self.browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Previous"]')
        except NoSuchElementException:
            print("Paginator error in the last page.")


if __name__ == "__main__":
    unittest.main()
