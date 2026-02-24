from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_progress_bar_1():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait=WebDriverWait(driver,10)

    try:
        # Open homepage
        driver.get("https://demoqa.com/")
        assert "demosit" in driver.title

        # Select Widgets
        elements_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//h5[text()='Widgets']/ancestor::a")))
        ActionChains(driver).click(elements_btn).perform()

        # Select Progress Bar
        elements_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Progress Bar']")))
        elements_scroll_origin=ScrollOrigin.from_element(elements_btn)
        ActionChains(driver).scroll_from_origin(elements_scroll_origin,0,200).pause(1).click(elements_btn).perform()

        wait.until(EC.presence_of_element_located((By.ID,"progressBarContainer")))
        ActionChains(driver).scroll_by_amount(0,-200).perform()

        # Check that progress bar is at 0%
        progress_bar=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#progressBar .progress-bar")))
        assert progress_bar.get_attribute("aria-valuenow")=="0"

        # Click Start
        start_btn=wait.until(EC.element_to_be_clickable((By.ID,"startStopButton")))
        ActionChains(driver).click(start_btn).perform()

        # Wait until progress bar reaches 100%
        wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR,"#progressBar .progress-bar").get_attribute("aria-valuenow")=="100")

        # Check that progress bar is at 100%
        progress_bar=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#progressBar .progress-bar")))
        assert progress_bar.get_attribute("aria-valuenow")=="100"

    finally:
        driver.quit()