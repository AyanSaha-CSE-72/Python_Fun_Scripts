from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open home page
    driver.get("http://localhost/agro_bondhu/index.html")
    time.sleep(5)
    
    # Test 1: Check if 4 buttons are clickable and navigate to correct pages
    test_passed = True
    
    # Test "Add Farmer" button
    try:
        driver.get("http://localhost/agro_bondhu/index.html")
        add_farmer_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Add Farmer')]"))
        )
        add_farmer_link.click()
        time.sleep(5)
        if "addfarmer.html" in driver.current_url or "farmerRegistrationForm" in driver.page_source:
            print("✓ Add Farmer page working")
        else:
            test_passed = False
            print("✗ Add Farmer page not working")
    except Exception as e:
        test_passed = False
        print(f"✗ Add Farmer button error: {e}")
    
    # Test "See All Farmers" button
    try:
        driver.get("http://localhost/agro_bondhu/index.html")
        see_farmers_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See All Farmers')]"))
        )
        see_farmers_link.click()
        time.sleep(5)
        if "see_all_farmers" in driver.current_url or "farmers" in driver.page_source.lower():
            print("✓ See All Farmers page working")
        else:
            test_passed = False
            print("✗ See All Farmers page not working")
    except Exception as e:
        test_passed = False
        print(f"✗ See All Farmers button error: {e}")
    
    # Test "Loan Status" button
    try:
        driver.get("http://localhost/agro_bondhu/index.html")
        loan_status_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Loan Status')]"))
        )
        loan_status_link.click()
        time.sleep(5)
        if "loan_status" in driver.current_url or "loan" in driver.page_source.lower():
            print("✓ Loan Status page working")
        else:
            test_passed = False
            print("✗ Loan Status page not working")
    except Exception as e:
        test_passed = False
        print(f"✗ Loan Status button error: {e}")
    
    # Test "Support Status" button
    try:
        driver.get("http://localhost/agro_bondhu/index.html")
        support_status_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Support Status')]"))
        )
        support_status_link.click()
        time.sleep(5)
        if "support_status" in driver.current_url or "support" in driver.page_source.lower():
            print("✓ Support Status page working")
        else:
            test_passed = False
            print("✗ Support Status page not working")
    except Exception as e:
        test_passed = False
        print(f"✗ Support Status button error: {e}")
    
    # Final result
    if test_passed:
        print("\n" + "="*40)
        print("All pages are working good")
        print("="*40)
    else:
        print("\n" + "="*40)
        print("Some pages are not working properly")
        print("="*40)

finally:
    driver.quit()
