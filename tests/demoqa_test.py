import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_demoqa_1():
    options=Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.maximize_window()
    wait=WebDriverWait(driver,10)

    def add_element(number):
        add_btn=wait.until(EC.visibility_of_element_located((By.ID,"addNewRecordButton")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",add_btn)
        time.sleep(0.2)
        add_btn.click()

        first_name_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#firstName.form-control")))
        first_name_field.clear()
        first_name_field.send_keys("Test"+str(number))
        last_name_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#lastName.form-control")))
        last_name_field.clear()
        last_name_field.send_keys("Testington")
        email_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#userEmail.form-control")))
        email_field.clear()
        email_field.send_keys("test"+str(number)+"@gmail.com")
        age_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#age.form-control")))
        age_field.clear()
        age_field.send_keys(20+number)
        salary_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#salary.form-control")))
        salary_field.clear()
        salary_field.send_keys(1000+number*100)
        department_field=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#department.form-control")))
        department_field.clear()
        department_field.send_keys("Testing")

        submit_btn=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#userForm #submit")))
        submit_btn.click()

    def get_page_count():
        text=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".pagination .col-auto strong"))).text
        return int(text.split(" of ")[1])

    def get_current_page():
        text=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".pagination .col-auto strong"))).text
        return int(text.split(" of ")[0])

    try:
        # Open homepage
        driver.get("https://demoqa.com/")
        assert "demosit" in driver.title

        # Select Elements
        elements_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//h5[text()='Elements']/ancestor::a")))
        elements_scroll_origin=ScrollOrigin.from_element(elements_btn)
        ActionChains(driver).scroll_from_origin(elements_scroll_origin,0,200).pause(1).click(elements_btn).perform()

        # Select Web Tables
        elements_btn=wait.until(EC.presence_of_element_located((By.XPATH,"//span[text()='Web Tables']/ancestor::a")))
        elements_btn.click()

        # Add elements
        num=0
        while get_page_count()==1:
            add_element(num)
            num+=1
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,".modal-dialog .modal-content #registration-form-modal")))
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,".modal-backdrop")))

        # Navigate to 2 page
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Next']")))
        next_btn=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Next']")))
        driver.execute_script("arguments[0].click();", next_btn)

        # Delete element
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"web-tables-wrapper")))
        driver.execute_script("window.scrollTo(0,0);")

        while get_current_page()==2:
            delete_buttons=driver.find_elements(By.XPATH,"//span[@title='Delete']")
            if not delete_buttons:
                break

            driver.execute_script("arguments[0].click();",delete_buttons[0])
            wait.until(EC.staleness_of(delete_buttons[0]))

        # Ensure pagination return to 1 page and that page number reduced to 1
        assert get_current_page()==1,"Did not return to page 1 after deleting page 2 items"
        assert get_page_count()==1,"There should be only 1 page left"

    finally:
        driver.quit()