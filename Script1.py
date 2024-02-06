import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ContactsPage:
    CONTACTS = 'Контакты'
    REGION = 'Республика Башкортостан'

    def __init__(self, browser):
        self.browser = browser

    def open(self):
        self.browser.get("https://sbis.ru/")
        contacts_link = self.browser.find_element(By.LINK_TEXT, self.CONTACTS)
        contacts_link.click()

    def get_region(self):
        region = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(@class,'sbis_ru-Region-Chooser__text') and contains(@class,'sbis_ru-link')]")))
        return region.text

    def check_text_on_page(self):
        try:
            element1 = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[text()='СБИС - Уфа']")))
            element2 = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[text()='СБИС | ЦЕНТР ВНЕДРЕНИЯ']")))
            text_found = True
        except:
            text_found = False
        return text_found

    def change_region(self):
        region_link = self.browser.find_element(By.XPATH,
                                                "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link' and text()='" + self.REGION + "']")
        region_link.click()
        time.sleep(2)  # Wait for the new page to load

    def verify_region_changed(self):
        region_link2 = self.browser.find_element(By.XPATH,
                                                 "//span[@class='sbis_ru-link' and text()='41 Камчатский край']")
        region_link2.click()
        time.sleep(5)
        assert "Камчатский край" in self.browser.find_element(By.TAG_NAME, 'body').text
        assert "41-kamchatskij" in self.browser.current_url

        try:
            element3 = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[text()='СБИС - Камчатка']")))
            text_found = True
        except:
            text_found = False
        assert text_found, "Текст 'СБИС - Камчатка' not found on the page"


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_sbis_contacts_page(browser):
    contacts_page = ContactsPage(browser)
    contacts_page.open()
    assert contacts_page.get_region() == contacts_page.REGION
    assert contacts_page.check_text_on_page()
    contacts_page.change_region()
    contacts_page.verify_region_changed()