import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""

        chrome_options = Options()

        if os.getenv("CI"):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

        driver_path = ChromeDriverManager().install()
        folder = os.path.dirname(driver_path)

        if "third_party_notices" in os.path.basename(driver_path).lower():
            candidates = [
                p for p in os.listdir(folder)
                if p.lower() in ("chromedriver.exe", "chromedriver")
            ]
            if candidates:
                driver_path = os.path.join(folder, candidates[0])
            else:
                raise RuntimeError(
                    f"chromedriver introuvable dans: {folder}\n"
                    f"install() a renvoyé: {driver_path}"
                )

        if os.getenv("CI") and not driver_path.lower().endswith(".exe"):
            try:
                os.chmod(driver_path, 0o755)
            except Exception:
                pass

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        driver.get("file://" + os.path.abspath("../src/index.html"))
        assert "Calculatrice" in driver.title

    def test_addition(self, driver):
        driver.get("file://" + os.path.abspath("../src/index.html"))

        driver.find_element(By.ID, "number1").clear()
        driver.find_element(By.ID, "number2").clear()
        driver.find_element(By.ID, "number1").send_keys("10")
        driver.find_element(By.ID, "number2").send_keys("5")
        driver.find_element(By.ID, "add").click()

        result = driver.find_element(By.ID, "result").text
        assert result == "15"

    def test_division_by_zero(self, driver):
        driver.get("file://" + os.path.abspath("../src/index.html"))

        driver.find_element(By.ID, "number1").clear()
        driver.find_element(By.ID, "number2").clear()
        driver.find_element(By.ID, "number1").send_keys("10")
        driver.find_element(By.ID, "number2").send_keys("0")
        driver.find_element(By.ID, "divide").click()

        result = driver.find_element(By.ID, "result").text.lower()
        assert "erreur" in result or "error" in result or "infinity" in result

    def test_all_operations(self, driver):
        driver.get("file://" + os.path.abspath("../src/index.html"))

        driver.find_element(By.ID, "number1").clear()
        driver.find_element(By.ID, "number2").clear()
        driver.find_element(By.ID, "number1").send_keys("8")
        driver.find_element(By.ID, "number2").send_keys("2")

        driver.find_element(By.ID, "subtract").click()
        assert driver.find_element(By.ID, "result").text == "6"

        driver.find_element(By.ID, "multiply").click()
        assert driver.find_element(By.ID, "result").text == "16"

        driver.find_element(By.ID, "divide").click()
        assert driver.find_element(By.ID, "result").text == "4"
