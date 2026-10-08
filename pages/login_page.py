"""Page Object for UTC's login and password-recovery screens."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_WAIT_SECONDS


class LoginPage:
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "userpwd")
    SUBMIT = (By.CSS_SELECTOR, "input.submit_login")
    REMEMBER_CHECKBOX = (By.ID, "persistent")
    REMEMBER_LABEL = (By.CSS_SELECTOR, "label[for='persistent']")
    FORGOT_PASSWORD = (By.CSS_SELECTOR, "a[href='/Login/GetPass']")
    GOOGLE_LOGIN = (By.CSS_SELECTOR, "a[href^='https://accounts.google.com/o/oauth2/auth']")
    RECOVERY_EMAIL = (By.CSS_SELECTOR, "input[placeholder='Địa chỉ Email']")
    RECOVERY_CAPTCHA = (By.CSS_SELECTOR, "input[placeholder='Mã bảo mật']")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_SECONDS)

    def open(self) -> "LoginPage":
        self.driver.get(BASE_URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def username_field(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.USERNAME))

    def password_field(self) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(self.PASSWORD))

    def submit_button(self) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(self.SUBMIT))

    def login_form_is_visible(self) -> bool:
        return all(
            element.is_displayed()
            for element in (self.username_field(), self.password_field(), self.submit_button())
        )

    def submit_login(self, username: str | None = None, password: str | None = None) -> None:
        if username is not None:
            self.username_field().send_keys(str(username))
        if password is not None:
            self.password_field().send_keys(str(password))
        self.submit_button().click()
        self.wait.until(EC.presence_of_element_located(self.USERNAME))

    def password_is_masked(self) -> bool:
        return self.password_field().get_attribute("type") == "password"

    def remember_me_can_toggle(self) -> bool:
        checkbox = self.driver.find_element(*self.REMEMBER_CHECKBOX)
        label = self.driver.find_element(*self.REMEMBER_LABEL)
        if checkbox.is_selected():
            return False
        label.click()
        selected_after_click = checkbox.is_selected()
        label.click()
        return selected_after_click and not checkbox.is_selected()

    def open_password_recovery(self) -> None:
        self.driver.find_element(*self.FORGOT_PASSWORD).click()
        self.wait.until(EC.url_contains("/Login/GetPass"))

    def recovery_form_is_visible(self) -> bool:
        return (
            "Lấy lại mật khẩu" in self.driver.title
            and self.driver.find_element(*self.RECOVERY_EMAIL).is_displayed()
            and self.driver.find_element(*self.RECOVERY_CAPTCHA).is_displayed()
        )

    def google_login_link_is_valid(self) -> bool:
        link = self.driver.find_element(*self.GOOGLE_LOGIN)
        return link.is_displayed() and "Đăng nhập bằng e-mail UTC" in link.text
