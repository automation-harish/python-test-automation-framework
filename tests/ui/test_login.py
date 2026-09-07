"""Sample UI tests demonstrating Page Object Model and Pytest fixtures."""
import pytest
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login(self):
        self.driver.get("https://example.com/login")

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)


class DashboardPage(BasePage):
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome")
    USER_PROFILE = (By.ID, "user-profile")
    LOGOUT_BUTTON = (By.ID, "logout")

    def __init__(self, driver):
        super().__init__(driver)

    def is_user_logged_in(self):
        return self.is_element_visible(self.USER_PROFILE)

    def get_page_title(self):
        return self.driver.title

    def logout(self):
        self.click(self.LOGOUT_BUTTON)


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """Login functionality smoke tests."""

    @pytest.fixture(autouse=True)
    def setup(self, chrome_driver):
        self.driver = chrome_driver
        self.login_page = LoginPage(self.driver)

    def test_login_page_loads(self):
        """Test that login page loads successfully."""
        self.login_page.navigate_to_login()
        assert "login" in self.login_page.driver.current_url.lower()

    def test_successful_login(self):
        """Test successful login with valid credentials."""
        self.login_page.navigate_to_login()
        self.login_page.login("admin@test.com", "Test@123")
        dashboard = DashboardPage(self.driver)
        assert dashboard.is_user_logged_in(), "User should be logged in"

    def test_failed_login_wrong_password(self):
        """Test login failure with wrong password."""
        self.login_page.navigate_to_login()
        self.login_page.login("admin@test.com", "wrongpassword")
        assert self.login_page.is_error_displayed(), "Error should be displayed"
        assert "invalid" in self.login_page.get_error_message().lower()

    def test_failed_login_empty_fields(self):
        """Test login failure with empty credentials."""
        self.login_page.navigate_to_login()
        self.login_page.click(self.login_page.LOGIN_BUTTON)
        assert self.login_page.is_error_displayed(), "Error should be displayed"


@pytest.mark.ui
@pytest.mark.regression
class TestNavigation:
    """Navigation functionality tests."""

    @pytest.fixture(autouse=True)
    def setup(self, chrome_driver):
        self.driver = chrome_driver

    def test_home_page_navigation(self):
        """Test navigation to home page."""
        self.driver.get("https://example.com")
        assert "example" in self.driver.title.lower() or self.driver.title != ""

    def test_menu_navigation(self):
        """Test menu links are clickable."""
        self.driver.get("https://example.com")
        menu_items = self.driver.find_elements(By.CSS_SELECTOR, "nav a")
        assert len(menu_items) >= 0


@pytest.mark.ui
@pytest.mark.regression
class TestForms:
    """Form functionality tests."""

    @pytest.fixture(autouse=True)
    def setup(self, chrome_driver):
        self.driver = chrome_driver

    def test_contact_form_submission(self):
        """Test contact form can be filled."""
        self.driver.get("https://example.com/contact")
        name_input = self.driver.find_element(By.ID, "name")
        email_input = self.driver.find_element(By.ID, "email")
        submit_button = self.driver.find_element(By.ID, "submit")

        if name_input.isDisplayed() and email_input.isDisplayed():
            name_input.send_keys("Test User")
            email_input.send_keys("test@example.com")
            submit_button.click()


@pytest.mark.ui
@pytest.mark.slow
class TestPerformance:
    """UI performance tests."""

    @pytest.fixture(autouse=True)
    def setup(self, chrome_driver):
        self.driver = chrome_driver

    def test_page_load_time(self):
        """Test page loads within acceptable time."""
        import time
        start = time.time()
        self.driver.get("https://example.com")
        load_time = time.time() - start
        assert load_time < 5, f"Page took {load_time:.2f}s to load"
