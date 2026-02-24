from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email="testuserartiom@example.com"
password="Password123!"

def test_purchase_flow_1():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait=WebDriverWait(driver,10)

    try:
        # Open homepage
        driver.get("https://demowebshop.tricentis.com")
        assert "Demo Web Shop" in driver.title

        # Login
        login_nav=wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"ico-login")))
        login_nav.click()

        email_input=wait.until(EC.visibility_of_element_located((By.ID,"Email")))
        email_input.clear()
        email_input.send_keys(email)

        password_input=driver.find_element(By.ID,"Password")
        password_input.clear()
        password_input.send_keys(password)

        login_button=driver.find_element(By.CLASS_NAME,"login-button")
        login_button.click()
        # Login check
        logout_nav=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"ico-logout")))
        assert logout_nav.is_displayed()

        # Go to Computers -> Desktops category
        computers_nav=wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Computers']")))
        computers_nav.click()

        desktops_nav=wait.until(EC.element_to_be_clickable((By.XPATH,"//h2[@class='title']/a[normalize-space()='Desktops']")))
        desktops_nav.click()

        # Desktops category verification
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"product-grid")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-grid .item-box")))

        # Selecting Build your own computer
        build_pc=wait.until(EC.element_to_be_clickable((By.XPATH,"//h2[@class='product-title']/a[normalize-space()='Build your own computer']")))
        build_pc.click()
        build_pc_hdd_select=wait.until(EC.element_to_be_clickable((By.ID,"product_attribute_16_3_6_18")))
        build_pc_hdd_select.click()
        add_to_cart=wait.until(EC.element_to_be_clickable((By.ID,"add-to-cart-button-16")))
        add_to_cart.click()

        # Go to Computers -> Desktops category
        computers_nav=wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Computers']")))
        computers_nav.click()

        desktops_nav=wait.until(EC.element_to_be_clickable((By.XPATH,"//h2[@class='title']/a[normalize-space()='Desktops']")))
        desktops_nav.click()

        # Desktops category verification
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"product-grid")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".product-grid .item-box")))

        # Selecting Build your own expensive computer
        build_pc=wait.until(EC.element_to_be_clickable((
            By.XPATH,"//h2[@class='product-title']/a[normalize-space()='Build your own expensive computer']"
        )))
        build_pc.click()
        add_to_cart=wait.until(EC.element_to_be_clickable((By.ID,"add-to-cart-button-74")))
        add_to_cart.click()

        # Go to shopping cart
        add_to_cart=wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"ico-cart")))
        add_to_cart.click()

        # Verify added products
        wait.until(lambda d:len(d.find_elements(By.CSS_SELECTOR,"tr.cart-item-row"))>=2)

        cart_rows=driver.find_elements(By.CSS_SELECTOR,"tr.cart-item-row")

        assert len(cart_rows)>=2,"Not enough cart items"

        product_names=[
            row.find_element(By.CSS_SELECTOR,".product-name").text.strip()
            for row in cart_rows
        ]

        assert "Build your own computer" in product_names
        assert "Build your own expensive computer" in product_names

        # Update quantity of first item
        qty_input=cart_rows[0].find_element(By.CSS_SELECTOR,"input.qty-input")
        qty_input.clear()
        qty_input.send_keys("2")

        update_cart_btn=wait.until(EC.element_to_be_clickable((By.NAME,"updatecart")))
        update_cart_btn.click()

        # Verify total price
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"tr.cart-item-row")))
        cart_rows=driver.find_elements(By.CSS_SELECTOR,"tr.cart-item-row")

        calculated_total=0.0
        for row in cart_rows:
            unit_price=float(row.find_element(By.CSS_SELECTOR,".product-unit-price").text)
            qty_value=int(row.find_element(By.CSS_SELECTOR,"input.qty-input").get_attribute("value"))
            row_subtotal=float(row.find_element(By.CSS_SELECTOR,".product-subtotal").text)
            assert unit_price*qty_value==row_subtotal,f"Row subtotal mismatch: expected {unit_price*qty_value}, got {row_subtotal}"
            calculated_total+=row_subtotal

        displayed_total=float(driver.find_element(By.CSS_SELECTOR, ".order-total strong").text)
        assert calculated_total==displayed_total,f"Cart total mismatch: expected {calculated_total}, got {displayed_total}"

        # Delete second item
        remove_checkbox=cart_rows[1].find_element(By.CSS_SELECTOR,"input[name='removefromcart']")
        remove_checkbox.click()

        update_cart_btn=wait.until(EC.element_to_be_clickable((By.NAME,"updatecart")))
        update_cart_btn.click()

        # Verify total price
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"tr.cart-item-row")))
        cart_rows=driver.find_elements(By.CSS_SELECTOR,"tr.cart-item-row")

        calculated_total=0.0
        for row in cart_rows:
            unit_price=float(row.find_element(By.CSS_SELECTOR,".product-unit-price").text)
            qty_value=int(row.find_element(By.CSS_SELECTOR,"input.qty-input").get_attribute("value"))
            row_subtotal=float(row.find_element(By.CSS_SELECTOR,".product-subtotal").text)
            assert unit_price*qty_value==row_subtotal,f"Row subtotal mismatch: expected {unit_price*qty_value}, got {row_subtotal}"
            calculated_total+=row_subtotal

        displayed_total=float(driver.find_element(By.CSS_SELECTOR,".order-total strong").text)
        assert calculated_total==displayed_total,f"Cart total mismatch: expected {calculated_total}, got {displayed_total}"

        # Check agreement
        tos_checkbox=wait.until(EC.visibility_of_element_located((By.ID,"termsofservice")))
        tos_checkbox.click()

        # Checkout
        checkout_btn=wait.until(EC.visibility_of_element_located((By.ID,"checkout")))
        checkout_btn.click()

        # Billing address
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-billing")))
        billing_address_select=wait.until(EC.visibility_of_element_located((By.ID,"billing-address-select")))

        selected_billing_address=billing_address_select.find_element(By.CSS_SELECTOR,"option:checked").text.strip()
        assert "Artiom Garbul" in selected_billing_address,f"Selected billing address: {selected_billing_address}"
        assert "123 Testing St" in selected_billing_address,f"Selected billing address: {selected_billing_address}"

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#billing-buttons-container .new-address-next-step-button")))
        continue_btn.click()

        # Shipping address
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-shipping")))
        shipping_address_select=wait.until(EC.visibility_of_element_located((By.ID,"shipping-address-select")))

        selected_shipping_address=shipping_address_select.find_element(By.CSS_SELECTOR,"option:checked").text.strip()
        assert "Artiom Garbul" in selected_shipping_address,f"Selected shipping address: {selected_shipping_address}"
        assert "123 Testing St" in selected_shipping_address,f"Selected shipping address: {selected_shipping_address}"

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#shipping-buttons-container .new-address-next-step-button")))
        continue_btn.click()

        # Shipping method
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-shipping-method")))
        shipping_method_select=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[value='Ground___Shipping.FixedRate']")))
        shipping_method_select.click()

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#shipping-method-buttons-container .shipping-method-next-step-button")))
        continue_btn.click()

        # Payment method
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-payment-method")))
        payment_method_select=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[value='Payments.CheckMoneyOrder']")))
        payment_method_select.click()

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#payment-method-buttons-container .payment-method-next-step-button")))
        continue_btn.click()

        # Payment information
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-payment-info")))
        payment_info_text=driver.find_element(By.ID,"checkout-step-payment-info").text

        assert "Tricentis GmbH" in payment_info_text,"Payment info missing company name"
        assert "1220 Vienna" in payment_info_text,"Payment info address is incorrect"
        assert "Check, Cashier's Check" in payment_info_text or "Cashier's Check" in payment_info_text,"Payment method details missing"

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#payment-info-buttons-container .payment-info-next-step-button")))
        continue_btn.click()

        # Confirm order
        wait.until(EC.visibility_of_element_located((By.ID,"checkout-step-confirm-order")))
        order_info_text=driver.find_element(By.ID,"checkout-step-confirm-order").text

        assert "Artiom Garbul" in order_info_text,"Billing/Shipping name missing"
        assert "123 Testing St" in order_info_text,"Address missing"
        assert "Andorra" in order_info_text,"Country missing"
        assert "Check / Money Order" in order_info_text,"Payment method missing"
        assert "Ground" in order_info_text,"Shipping method missing"

        continue_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#confirm-order-buttons-container .confirm-order-next-step-button")))
        continue_btn.click()

        # Verify order success
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"order-completed")))
        order_text=driver.find_element(By.CLASS_NAME,"order-completed").text

        assert "Your order has been successfully processed!" in order_text,"Order failed"

        # Logout
        logout_nav=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"ico-logout")))
        logout_nav.click()

        # Logout check
        login_nav=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"ico-login")))
        assert login_nav.is_displayed()
    finally:
        driver.quit()