# Test Case: Apply valid coupon code 'FREESHIP' with express shipping selected.

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Setup Chrome WebDriver (uses webdriver_manager to handle chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless for CI environments
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    wait = WebDriverWait(driver, 10)  # Explicit wait helper

    try:
        # Load the local checkout.html file
        file_path = "C:/Users/Pojesh/Documents/GitHub/Autonomous-QA-Agent/Project Assets/checkout.html"
        driver.get(file_path)

        #driver.get("https://pojesh.github.io/Test-Site/index.html")

        # 1. Add a product to the cart (Mechanical Keyboard)
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-btn-1")))
        add_btn.click()

        # Wait until the cart shows the item (empty-cart-msg should disappear)
        wait.until(EC.invisibility_of_element_located((By.ID, "empty-cart-msg")))

        # 2. Select Express Shipping
        express_radio = wait.until(EC.element_to_be_clickable((By.ID, "shipping-express")))
        express_radio.click()

        # 3. Apply the FREESHIP coupon code
        discount_input = wait.until(EC.presence_of_element_located((By.ID, "discount-code")))
        discount_input.clear()
        discount_input.send_keys("FREESHIP")

        apply_btn = wait.until(EC.element_to_be_clickable((By.ID, "apply-coupon")))
        apply_btn.click()

        # 4. Assertions

        # 4.1 Coupon message appears with correct text and green color
        coupon_msg = wait.until(EC.visibility_of_element_located((By.ID, "coupon-message")))
        assert "Coupon 'FREESHIP' applied!" in coupon_msg.text, "Coupon message text mismatch."

        # Verify the message has the green text class
        msg_classes = coupon_msg.get_attribute("class")
        assert "text-green-600" in msg_classes, "Coupon message is not green."

        # 4.2 Shipping cost is $0.00 regardless of express selection
        shipping_el = driver.find_element(By.ID, "summary-shipping")
        shipping_value = shipping_el.text.strip()
        assert shipping_value == "0.00", f"Expected shipping 0.00, got {shipping_value}"

        # 4.3 Subtotal remains unchanged (should be 120.00 after adding one keyboard)
        subtotal_el = driver.find_element(By.ID, "summary-subtotal")
        subtotal_value = subtotal_el.text.strip()
        assert subtotal_value == "120.00", f"Expected subtotal 120.00, got {subtotal_value}"

        # 4.4 Discount row should be hidden (no discount applied)
        discount_row = driver.find_element(By.ID, "discount-row")
        assert discount_row.value_of_css_property("display") == "none", "Discount row should be hidden."

        print("Test TC002 passed: FREESHIP coupon applied correctly with express shipping.")

    except AssertionError as ae:
        print(f"Assertion failed: {ae}")
    except Exception as e:
        print(f"An error occurred during test execution: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()