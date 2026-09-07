"""Pytest fixtures for test automation framework."""
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import yaml


def load_config():
    """Load configuration from config.yaml."""
    config_path = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def config():
    """Load test configuration."""
    return load_config()


@pytest.fixture(scope="function")
def chrome_driver(config):
    """Chrome WebDriver fixture."""
    options = webdriver.ChromeOptions()
    if config.get("browser", {}).get("headless", True):
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(config.get("browser", {}).get("implicit_wait", 10))
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driver(request):
    """Dynamic driver fixture based on browser parameter."""
    browser = request.param if hasattr(request, "param") else "chrome"
    config = load_config()
    browser_cfg = config.get("browser", {})

    options = webdriver.ChromeOptions()
    if browser_cfg.get("headless", True):
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(browser_cfg.get("implicit_wait", 10))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def api_base_url(config):
    """API base URL from config."""
    return config.get("api_base_url")


@pytest.fixture
def api_client(api_base_url):
    """API client fixture."""
    from src.api.clients.api_client import APIClient
    return APIClient(base_url=api_base_url)
