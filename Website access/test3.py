from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open Add Farmer page
    driver.get("http://localhost/agro_bondhu/addfarmer.html")
    time.sleep(2)
    
    # Wait for form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "farmerRegistrationForm"))
    )
    
    # Test: Invalid phone number (less than 11 digits)
    print("Testing with invalid phone number (123)...")
    
    # Fill out the form with invalid phone number
    # Full Name
    farmer_name = driver.find_element(By.ID, "farmerName")
    farmer_name.clear()
    farmer_name.send_keys("করিম সাহেব")
    time.sleep(0.5)
    
    # Mobile Number (INVALID - only 3 digits)
    mobile_number = driver.find_element(By.ID, "mobileNumber")
    mobile_number.clear()
    mobile_number.send_keys("123")
    time.sleep(0.5)
    
    # Address
    address = driver.find_element(By.ID, "address")
    address.clear()
    address.send_keys("রাজশাহী জেলা")
    time.sleep(0.5)
    
    # Try to submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    
    print("Attempting to submit form with invalid phone number...")
    time.sleep(1)
    
    # Check if form is disabled or shows validation message
    # The HTML has pattern="[0-9]{11}" which should prevent submission
    
    # Try clicking submit and see if it's prevented by HTML5 validation
    submit_button.click()
    time.sleep(2)
    
    # Check if an alert appears or if the form validation message shows
    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        print(f"Alert received: {alert_text}")
    except:
        # Check if page still on the same URL (form not submitted)
        if "addfarmer.html" in driver.current_url:
            # Try to find validation message or check mobile field validity
            mobile_field = driver.find_element(By.ID, "mobileNumber")
            
            # Try to check the validity state via JavaScript
            is_valid = driver.execute_script("return document.getElementById('mobileNumber').checkValidity();")
            
            if not is_valid:
                print("\n" + "="*50)
                print("✓ Form validation working correctly!")
                print("You should Enter a valid Number")
                print("Phone number validation successful")
                print("="*50)
            else:
                print("Unexpected: Form validation did not prevent invalid input")
        else:
            print("Form was submitted despite invalid phone number")

finally:
    time.sleep(2)
    driver.quit()
