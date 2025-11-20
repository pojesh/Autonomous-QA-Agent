from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://pojesh.github.io/Test-Site/")
        time.sleep(1)
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        sys.exit(1)

    try:
        add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to Cart')]")))
        add_to_cart_btn.click()
        time.sleep(1)
    except Exception as e:
        print(f"Error clicking Add to Cart: {e}")
        driver.quit()
        sys.exit(1)

    try:
        wait.until(lambda d: d.find_element(By.XPATH, "//div[contains(text(),'Subtotal')]/following-sibling::*[1]").text.strip() != "$0.00")
        subtotal_elem = driver.find_element(By.XPATH, "//div[contains(text(),'Subtotal')]/following-sibling::*[1]")
        subtotal_text = subtotal_elem.text.strip()
    except Exception as e:
        print(f"Error locating subtotal: {e}")
        driver.quit()
        sys.exit(1)

    try:
        express_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Express ($10.00)')]")))
        express_label.click()
        time.sleep(1)
    except Exception as e:
        print(f"Error selecting Express shipping: {e}")
        driver.quit()
        sys.exit(1)

    try:
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[contains(text(),'Shipping')]/following-sibling::*[1]"), "$10.00"))
        shipping_elem = driver.find_element(By.XPATH, "//div[contains(text(),'Shipping')]/following-sibling::*[1]")
        shipping_text = shipping_elem.text.strip()
    except Exception as e:
        print(f"Error locating shipping cost: {e}")
        driver.quit()
        sys.exit(1)

    try:
        total_elem = driver.find_element(By.XPATH, "//div[contains(text(),'Total')]/following-sibling::*[1]")
        total_text = total_elem.text.strip()
        subtotal_value = float(subtotal_text.replace("$", "").replace(",", ""))
        shipping_value = float(shipping_text.replace("$", "").replace(",", ""))
        total_value = float(total_text.replace("$", "").replace(",", ""))
        expected_total = subtotal_value + shipping_value
        if abs(total_value - expected_total) > 0.01:
            print(f"Total mismatch: expected {expected_total}, got {total_value}")
            driver.quit()
            sys.exit(1)
    except Exception as e:
        print(f"Error verifying total: {e}")
        driver.quit()
        sys.exit(1)

    print("Test passed: Shipping cost and total are correct.")
    driver.quit()

if __name__ == "__main__":
    main()