import time
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CONTACTS = 'Контакты'
TEXT1 = 'Сила в людях'


class MainPage:
    def __init__(self, browser):
        self.browser = browser

    def open_contacts_page(self):
        self.browser.get("https://sbis.ru/")
        contacts_link = self.browser.find_element(By.LINK_TEXT, CONTACTS)
        contacts_link.click()


class ContactsPage:
    def __init__(self, browser):
        self.browser = browser

    def open_tensor_website(self):
        tensor_banner = self.browser.find_element(By.XPATH, "//a[@title='tensor.ru']")
        main_window = self.browser.current_window_handle

        tensor_banner.click()
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))

        all_windows = self.browser.window_handles
        new_window = [window for window in all_windows if window != main_window][0]
        self.browser.switch_to.window(new_window)


class TensorAboutPage:
    def __init__(self, browser):
        self.browser = browser

    def verify_text_element_is_displayed(self):
        element_with_text = self.browser.find_element(By.XPATH, '//p[contains(text(),"Сила в людях")]')
        if element_with_text.is_displayed():
            return True
        else:
            return False

    def go_to_more_info_page(self):
        more_info_link = self.browser.find_element(By.LINK_TEXT, "Подробнее")
        link_url = more_info_link.get_attribute('href')
        more_info_link.click()
        WebDriverWait(self.browser, 10).until(EC.url_to_be(link_url))
        self.browser.get("https://tensor.ru/about")



@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_open_tensor_about_page(browser):
    main_page = MainPage(browser)
    contacts_page = ContactsPage(browser)
    tensor_about_page = TensorAboutPage(browser)

    main_page.open_contacts_page()
    contacts_page.open_tensor_website()

    assert tensor_about_page.verify_text_element_is_displayed(), "Element is not displayed on the page"

    tensor_about_page.go_to_more_info_page()

    images = browser.find_elements(By.CLASS_NAME, 'tensor_ru-About__block3-image-filter')
    assert len(images) > 0, "No images found with class 'tensor_ru-About__block3-image-filter'"
    first_image_size = (images[0].size['width'], images[0].size['height'])
    for image in images:
        assert (image.size['width'], image.size['height']) == first_image_size