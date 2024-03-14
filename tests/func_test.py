import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasicInstallTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', options=options)
        time.sleep(5)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get("http://mywebsite:8000")
        self.assertIn("База українських кріейтерів", self.browser.title)

    def test_home_page_header(self):
        self.browser.get("http://mywebsite:8000")
        header_element = self.browser.find_element(By.TAG_NAME, "h1")
        header_text = header_element.text
        self.assertIn("База українських кріейтерів", header_text)

    def test_pagination_with_category_selection(self):
        self.browser.get("http://mywebsite:8000")
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
        assert self.browser.current_url == "http://mywebsite:8000/youtuber_list/?page=2"
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

    def test_add_and_delete_comment_authorized(self):
        self.browser.get("http://mywebsite:8000/login/")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        try:
            username_input = self.browser.find_element(By.NAME, "username")
            password_input = self.browser.find_element(By.NAME, "password")
        except NoSuchElementException:
            print("Login form does not exist.")

        username_input.send_keys('test_user')
        password_input.send_keys('test_password')
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        self.browser.get(f"http://mywebsite:8000/youtuber_list/gamewizua/")

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        comment_input = self.browser.find_element(By.NAME, "text")
        comment_input.send_keys('This is a test comment')
        send_button = self.browser.find_element(By.XPATH, '//button[text()="Додати коментар"]')
        send_button.click()
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'comment-1')))

        test_card = self.browser.find_element(By.ID, 'comment-1')
        comment_text = test_card.find_element(By.CSS_SELECTOR, '.card-text').text

        self.assertEqual(comment_text, 'This is a test comment')

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'delete-comment-button')))
        delete_button = self.browser.find_element(By.ID, 'delete-comment-button')
        delete_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))
        success_message = self.browser.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertEqual(success_message, 'Коментар видалено.')

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.XPATH, "//*[contains(text(), 'This is a test comment')]")


    def test_comment_unauthorized(self):
        self.browser.get("http://mywebsite:8000/youtuber_list/gamewizua/")

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        comment_input = self.browser.find_element(By.NAME, "text")
        comment_input.send_keys('This is a test comment')
        send_button = self.browser.find_element(By.XPATH, '//button[text()="Додати коментар"]')
        send_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger')))

        error_message = self.browser.find_element(By.CLASS_NAME, 'alert-danger').text

        self.assertEqual(error_message, 'Будь-ласка увійдіть, щоб залишити коментар.')

    def test_add_teg(self):
        self.browser.get("http://mywebsite:8000/youtuber_list/test_slug_name/")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#tag')))
        tag_input = self.browser.find_element(By.CSS_SELECTOR, '#id_tag')
        submit_button = self.browser.find_element(By.CSS_SELECTOR, '#submit-tag')
        tag_input.send_keys('test tag')
        submit_button.submit()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="tag-test tag"]')))
        max_attempts = 10
        while max_attempts > 0:
            try:
                tag_text = self.browser.find_element(By.XPATH, '//button[@id="tag-test tag"]').text
                self.assertIn('test tag', tag_text)
                break
            except StaleElementReferenceException:
                max_attempts -= 1
                time.sleep(1)


if __name__ == "__main__":
    unittest.main()
