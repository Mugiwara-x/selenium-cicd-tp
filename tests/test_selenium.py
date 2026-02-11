import os
import sys
import stat
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
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

        candidates = []
        for name in ("chromedriver.exe", "chromedriver"):
            p = os.path.join(folder, name)
            if os.path.exists(p):
                candidates.append(p)

        if candidates:
            driver_path = candidates[0]
        else:
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower() in ("chromedriver.exe", "chromedriver"):
                        driver_path = os.path.join(root, f)
                        candidates = [driver_path]
                        break
                if candidates:
                    break

        if not candidates:
            raise RuntimeError(
                f"chromedriver introuvable dans: {folder}\n"
                f"install() a renvoyé: {driver_path}"
            )

        # ✅ FIX 3: CI Linux -> Permission denied si pas exécutable
        if os.getenv("CI") and not sys.platform.startswith("win"):
            mode = os.stat(driver_path).st_mode
            os.chmod(driver_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)

        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
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

        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
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
            ("divide", "8", "2", "4"),
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
