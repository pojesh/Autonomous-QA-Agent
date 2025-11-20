import re
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestDiscountCodeFeature(unittest.TestCase):
    """Test case TC001 – Apply valid SAVE15 code to a cart with subtotal $120.00"""

    @classmethod
    def setUpClass(cls):
        # Initialize Chrome WebDriver (assumes chromedriver is in PATH or uses webdriver_manager)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run headless for CI environments
        options.add_argument("--disable-gpu")
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        cls.driver.maximize_window()
        # Replace with the actual checkout page URL
        cls.base_url = "http://localhost:8000/checkout"
        cls.driver.get(cls.base_url)
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def _extract_amount(self, text):
        """Utility to extract numeric amount from a string like '$120.00'."""
        match = re.search(r"[-]?\$([0-9,.]+)", text)
        return float(match.group(1).replace(",", "")) if match else None

    def test_apply_valid_save15_discount(self):
        driver = self.driver
        wait = self.wait

        try:
            # 1. Add Mechanical Keyboard ($120.00) to the cart
            # Locate the product container by its name and then find the sibling "Add to Cart" button
            product_name = "Mechanical Keyboard"
            add_to_cart_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//div[contains(text(), '{product_name}')]/following::button[normalize-space()='Add to Cart'][1]"
                    )
                )
            )
            add_to_cart_button.click()

            # 2. Verify cart subtotal updates to $120.00
            subtotal_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'subtotal') or contains(@class,'subtotal')]"))
            )
            subtotal_text = subtotal_elem.text
            self.assertAlmostEqual(self._extract_amount(subtotal_text), 120.00,
                                   msg=f"Expected subtotal $120.00, got {subtotal_text}")

            # 3. Enter discount code "SAVE15" and apply
            discount_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder,'Discount') or contains(@id,'discount')]"))
            )
            discount_input.clear()
            discount_input.send_keys("SAVE15")

            apply_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Apply' and not(contains(@disabled,'disabled'))]")
                )
            )
            apply_button.click()

            # 4. Wait for discount to be applied and verify discount amount
            discount_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'discount') or contains(@class,'discount')]"))
            )
            discount_text = discount_elem.text
            discount_amount = self._extract_amount(discount_text)
            self.assertAlmostEqual(discount_amount, 18.00,
                                   msg=f"Expected discount $18.00, got {discount_text}")

            # 5. Verify subtotal remains $120.00 after discount
            subtotal_text_after = subtotal_elem.text
            self.assertAlmostEqual(self._extract_amount(subtotal_text_after), 120.00,
                                   msg=f"Subtotal should remain $120.00 after discount, got {subtotal_text_after}")

            # 6. Verify shipping cost remains $0.00 (standard free)
            shipping_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'shipping') or contains(@class,'shipping')]"))
            )
            shipping_text = shipping_elem.text
            shipping_amount = self._extract_amount(shipping_text)
            self.assertAlmostEqual(shipping_amount, 0.00,
                                   msg=f"Expected shipping $0.00, got {shipping_text}")

            # 7. Verify total equals $102.00 (120 - 18 + 0)
            total_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'total') or contains(@class,'total')]"))
            )
            total_text = total_elem.text
            total_amount = self._extract_amount(total_text)
            self.assertAlmostEqual(total_amount, 102.00,
                                   msg=f"Expected total $102.00, got {total_text}")

            # 8. (Optional) Proceed to payment to confirm success message
            pay_now_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-primary') and normalize-space()='Pay Now']")
                )
            )
            # Fill required fields for payment
            name_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='fullName' or @placeholder='Full Name']"))
            )
            name_input.clear()
            name_input.send_keys("John Doe")

            email_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='email' or @placeholder='Email Address']"))
            )
            email_input.clear()
            email_input.send_keys("john.doe@example.com")

            address_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//textarea[@name='address' or @placeholder='Shipping Address']"))
            )
            address_input.clear()
            address_input.send_keys("123 Main St, Anytown, USA")

            # Select shipping method if needed (default is standard)
            shipping_method_radio = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@name='shippingMethod' and @value='standard']")
                )
            )
            shipping_method_radio.click()

            # Select payment method (credit card)
            payment_method_radio = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@name='paymentMethod' and @value='credit_card']")
                )
            )
            payment_method_radio.click()

            # Click Pay Now
            pay_now_button.click()

            # Wait for success message container
            success_msg = wait.until(
                EC.visibility_of_element_located((By.ID, "success-message"))
            )
            self.assertIn("Payment Successful!", success_msg.text,
                          msg="Success message not displayed after payment.")

        except Exception as e:
            self.fail(f"Test failed due to exception: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)