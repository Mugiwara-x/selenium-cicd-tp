import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os


class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""

        chrome_options = Options()

        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

        driver_path = ChromeDriverManager().install()

        if not driver_path.lower().endswith("chromedriver.exe"):
            folder = os.path.dirname(driver_path)
            candidates = [p for p in os.listdir(folder) if p.lower() == "chromedriver.exe"]

            if candidates:
                driver_path = os.path.join(folder, candidates[0])
            else:
                raise RuntimeError(
                    f"chromedriver.exe introuvable dans: {folder}\n"
                    f"install() a renvoyé: {driver_path}"
                )

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)

        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        """Test 01: Vérifier que la page se charge correctement"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        assert "Calculatrice Simple" in driver.title
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "Résultat: 15" in result.text

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        assert "Erreur: Division par zéro" in result.text

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]

        for op, num1, num2, expected in operations:
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num2").clear()

            driver.find_element(By.ID, "num1").send_keys(num1)
            driver.find_element(By.ID, "num2").send_keys(num2)

            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)

            driver.find_element(By.ID, "calculate").click()

            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )

            assert f"Résultat: {expected}" in result.text

            time.sleep(1)


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
