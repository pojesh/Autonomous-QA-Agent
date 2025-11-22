# Test Case: Enter an email address containing whitespace characters (e.g., user @example.com) and submit the form.

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Setup Chrome driver (using webdriver_manager for convenience)
    options = webdriver.ChromeOptions()
    # Allow access to local files
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--disable-web-security")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Build absolute path to checkout.html and load it
        html_path = os.path.abspath("checkout.html")
        driver.get(f"file://{html_path}")

        wait = WebDriverWait(driver, 10)

        # ------------------------------------------------------------------
        # 1. Add a product to the cart to avoid cart-empty validation
        # ------------------------------------------------------------------
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-btn-1")))
        add_btn.click()

        # Wait until the cart items container updates (product appears)
        wait.until(EC.presence_of_element_located((By.ID, "cart-items-container")))

        # ------------------------------------------------------------------
        # 2. Fill in the checkout form with an invalid email (contains whitespace)
        # ------------------------------------------------------------------
        # Full Name
        full_name_input = wait.until(EC.presence_of_element_located((By.ID, "full-name")))
        full_name_input.clear()
        full_name_input.send_keys("John Doe")

        # Email with whitespace
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys("user @example.com")  # Note the space

        # Shipping Address
        address_input = driver.find_element(By.ID, "address")
        address_input.clear()
        address_input.send_keys("123 Main St, Anytown")

        # ------------------------------------------------------------------
        # 3. Submit the form
        # ------------------------------------------------------------------
        pay_now_btn = driver.find_element(By.ID, "pay-now-btn")
        pay_now_btn.click()

        # ------------------------------------------------------------------
        # 4. Assertions
        # ------------------------------------------------------------------
        # 4a. Error message should be displayed
        error_email = wait.until(EC.visibility_of_element_located((By.ID, "error-email")))
        assert error_email.is_displayed(), "Error message for email is not displayed."

        # 4b. Email input should have 'input-error' class
        email_classes = email_input.get_attribute("class")
        assert "input-error" in email_classes, "Email input does not have 'input-error' class."

        # 4c. Success message should remain hidden (form submission blocked)
        success_msg = driver.find_element(By.ID, "success-message")
        # The success message has class 'hidden' when not shown
        assert "hidden" in success_msg.get_attribute("class"), "Success message is unexpectedly visible."

        # 4d. Pay Now button should still be enabled (not disabled by processing)
        assert pay_now_btn.is_enabled(), "Pay Now button is disabled after failed validation."

        print("Test TC_EMAIL_04 passed: Validation error displayed and form submission blocked as expected.")

    except AssertionError as ae:
        print(f"Assertion failed: {ae}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Give a short pause to observe results before closing (optional)
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()