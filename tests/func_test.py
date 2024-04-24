import os
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


SELENIUM_SERVER_URL = os.environ.get('SELENIUM_SERVER_URL')
MYWEBSITE_URL = os.environ.get("MYWEBSITE_URL")


class BasicInstallTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Remote(command_executor=SELENIUM_SERVER_URL, options=options)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get(MYWEBSITE_URL)
        self.assertIn("База українських кріейтерів", self.browser.title)

    def test_home_page_header(self):
        self.browser.get(MYWEBSITE_URL)
        header_element = self.browser.find_element(By.TAG_NAME, "h1")
        header_text = header_element.text
        self.assertIn("База українських кріейтерів", header_text)

    def test_pagination_with_category_selection(self):
        self.browser.get(MYWEBSITE_URL)

        checkboxes_element_name = 'categories'
        search_button_element_css = 'button.btn.btn-primary[type="submit"]'
        next_button_element_css = 'a[aria-label="Next"]'
        first_button_element_css = 'a[aria-label="First"]'
        last_button_element_css = 'a[aria-label="Last"]'
        previous_button_element_css = 'a[aria-label="Previous"]'


        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                search_button_element_css)))

        checkboxes = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.NAME, checkboxes_element_name))
        )

        checkboxes = self.browser.find_elements(By.NAME, checkboxes_element_name)
        for checkbox in checkboxes[:5]:
            checkbox.click()

        search_button = self.browser.find_element(By.CSS_SELECTOR,
                                                  search_button_element_css)

        search_button.submit()
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, next_button_element_css)))
        try:
            next_button = self.browser.find_element(By.CSS_SELECTOR, next_button_element_css)
            last_button = self.browser.find_element(By.CSS_SELECTOR, last_button_element_css)
        except NoSuchElementException:
            print("Paginator error in the First page.")

        next_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, first_button_element_css)))
        assert self.browser.current_url == MYWEBSITE_URL + "/youtuber_list/?page=2"
        try:
            first_button = self.browser.find_element(By.CSS_SELECTOR, first_button_element_css)
            last_button = self.browser.find_element(By.CSS_SELECTOR, last_button_element_css)
            previous_button = self.browser.find_element(By.CSS_SELECTOR,
                                                        previous_button_element_css)
            next_button = self.browser.find_element(By.CSS_SELECTOR, next_button_element_css)
        except NoSuchElementException:
            print("Paginator error in the second page.")

        last_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, first_button_element_css)))
        try:
            first_button = self.browser.find_element(By.CSS_SELECTOR, first_button_element_css)
            previous_button = self.browser.find_element(By.CSS_SELECTOR,
                                                        previous_button_element_css)
        except NoSuchElementException:
            print("Paginator error in the last page.")

    def test_add_and_delete_comment_authorized(self):
        self.browser.get(MYWEBSITE_URL + "/login/")

        username_input_element_name = "username"
        password_input_element_name = "password"
        comment_input_element_name = "text"
        test_card_element_id = 'comment-1'
        delete_button_element_id = 'delete-comment-button'
        success_message_element_class = 'alert-success'
        test_comment_text = 'This is a test comment'

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, username_input_element_name)))
        try:
            username_input = self.browser.find_element(By.NAME, username_input_element_name)
            password_input = self.browser.find_element(By.NAME, password_input_element_name)
        except NoSuchElementException:
            print("Login form does not exist.")

        username_input.send_keys('test_user')
        password_input.send_keys('test_password')
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        self.browser.get(MYWEBSITE_URL + "/youtuber_list/gamewizua/")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME,comment_input_element_name)))
        comment_input = self.browser.find_element(By.NAME, comment_input_element_name)
        comment_input.send_keys(test_comment_text)
        send_button = self.browser.find_element(By.XPATH, '//button[text()="Додати коментар"]')
        send_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID,test_card_element_id)))

        test_card = self.browser.find_element(By.ID, test_card_element_id)
        comment_text = test_card.find_element(By.CSS_SELECTOR, '.card-text').text

        self.assertEqual(comment_text, test_comment_text)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, delete_button_element_id)))
        delete_button = self.browser.find_element(By.ID, delete_button_element_id)
        delete_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, success_message_element_class)))
        success_message = self.browser.find_element(
            By.CLASS_NAME, success_message_element_class).text
        self.assertEqual(success_message, 'Коментар видалено.')

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.XPATH, f"//*[contains(text(), '{test_comment_text}')]")

    def test_comment_unauthorized(self):
        self.browser.get(MYWEBSITE_URL + "/youtuber_list/gamewizua/")

        comment_input_element_name = 'text'
        error_message_element_class = 'alert-danger'

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, comment_input_element_name)))
        comment_input = self.browser.find_element(By.NAME, comment_input_element_name)
        comment_input.send_keys('This is a test comment')
        send_button = self.browser.find_element(By.XPATH, '//button[text()="Додати коментар"]')
        send_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, error_message_element_class)))

        error_message = self.browser.find_element(By.CLASS_NAME, error_message_element_class).text

        self.assertEqual(error_message, 'Будь-ласка увійдіть, щоб залишити коментар.')

    def test_add_tag(self):
        self.browser.get(MYWEBSITE_URL + "/youtuber_list/test_slug_name/")

        test_tag_text = 'test tag'

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#tag')))
        tag_input = self.browser.find_element(By.CSS_SELECTOR, '#id_tag')
        submit_button = self.browser.find_element(By.CSS_SELECTOR, '#submit-tag')
        tag_input.send_keys(test_tag_text)
        submit_button.submit()

        element_locator = (By.XPATH, '//button[@id="tag-test tag"]')
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(element_locator, test_tag_text)
        )
        element = self.browser.find_element(*element_locator)
        element_tag_text = element.text
        self.assertIn(test_tag_text, element_tag_text)

    def test_search_channel(self):
        self.browser.get(MYWEBSITE_URL + "/search/")

        search_button_id = 'search'
        channel_title_id = 'channel-title-1'
        channel_description_id = 'channel-description-1'

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, search_button_id)))

        search_input = self.browser.find_element(By.ID, search_button_id)
        search_input.send_keys('test_channel_description')
        search_button = self.browser.find_element(By.CSS_SELECTOR,
                                                  'input[type="submit"][value="Пошук"]')
        search_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, channel_title_id)))

        title_element = self.browser.find_element(By.ID, channel_title_id)
        description_element = self.browser.find_element(By.ID, channel_description_id)

        self.assertEqual(title_element.text, 'test_channel_title')
        self.assertEqual(description_element.text, 'test_channel_description')


if __name__ == "__main__":
    unittest.main()
