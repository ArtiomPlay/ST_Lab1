import time
from tokenize import String

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dynamic_properties_1():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait=WebDriverWait(driver,20)

    try:
        # Open homepage
        driver.get("https://demoqa.com/")
        assert "demosit" in driver.title

        # Select Elements
        elements_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//h5[text()='Elements']/ancestor::a")))
        ActionChains(driver).click(elements_btn).perform()

        # Select Dynamic Properties
        elements_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Dynamic Properties']")))
        elements_scroll_origin=ScrollOrigin.from_element(elements_btn)
        ActionChains(driver).scroll_from_origin(elements_scroll_origin,0,200).pause(1).click(elements_btn).perform()

        wait.until(EC.presence_of_element_located((By.ID,"enableAfter")))
        ActionChains(driver).scroll_by_amount(0,-200).perform()

        # Check that button “Will enable 5 seconds” is not clickable
        enable_btn=driver.find_element(By.ID,"enableAfter")
        assert not enable_btn.is_enabled()

        # Wait until button “Will enable 5 seconds” is clickable
        wait.until(EC.element_to_be_clickable((By.ID,"enableAfter")))
        assert enable_btn.is_enabled()

        # Check that button “Visible After 5 Seconds” is visible
        visible_after=wait.until(EC.visibility_of_element_located((By.ID,"visibleAfter")))
        assert visible_after.is_displayed()
        
    finally:
        driver.quit()