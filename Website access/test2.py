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
    
    # Fill out the form with valid data
    print("Filling form with valid data...")
    
    # Full Name
    farmer_name = driver.find_element(By.ID, "farmerName")
    farmer_name.clear()
    farmer_name.send_keys("রহিম আহমেদ")
    time.sleep(0.5)
    
    # Mobile Number (11 digits)
    mobile_number = driver.find_element(By.ID, "mobileNumber")
    mobile_number.clear()
    mobile_number.send_keys("01712345678")
    time.sleep(0.5)
    
    # Address
    address = driver.find_element(By.ID, "address")
    address.clear()
    address.send_keys("গাজীপুর জেলা, বাঘেরহাট গ্রাম")
    time.sleep(0.5)
    
    # Loan Status
    loan_status = driver.find_element(By.ID, "loanStatus")
    loan_status.send_keys("pending")
    time.sleep(0.5)
    
    # Loan Amount
    loan_amount = driver.find_element(By.ID, "loanAmount")
    loan_amount.clear()
    loan_amount.send_keys("50000")
    time.sleep(0.5)
    
    # Support Status
    support_status = driver.find_element(By.ID, "supportStatus")
    support_status.send_keys("pending")
    time.sleep(0.5)
    
    # Support Type
    support_type = driver.find_element(By.ID, "supportType")
    support_type.clear()
    support_type.send_keys("ফসল সংক্রান্ত পরামর্শ")
    time.sleep(0.5)
    
    print("Form filled successfully!")
    
    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(3)
    
    # Wait for success message (alert or page change)
    try:
        # Check for alert
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        
        if "success" in alert_text.lower() or "saved" in alert_text.lower() or "Added" in alert_text:
            print("\n" + "="*50)
            print("✓ SUCCESSFUL MESSAGE:")
            print(f"  {alert_text}")
            print("="*50)
        else:
            print(f"Alert received: {alert_text}")
    except:
        # If no alert, check page content
        page_source = driver.page_source.lower()
        if "success" in page_source or "saved" in page_source or "added" in page_source:
            print("\n" + "="*50)
            print("✓ Form submitted successfully!")
            print("="*50)
        else:
            print("Form submitted but status unclear")

finally:
    time.sleep(2)
    driver.quit()
