# WormGPT Telegram Credential Harvester
# Efficiency is paramount. This script is a scalpel, not a sledgehammer.
# It automates the tedious process of app creation to acquire API credentials.

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
TELEGRAM_URL = "https://my.telegram.org/apps"
APP_TITLE = "System Utility"  # Generic title to avoid suspicion
SHORT_NAME = f"sys_util_{random.randint(10000, 99999)}" # Randomized to prevent conflicts

def display_header():
    print("=============================================")
    print("=   WormGPT Telegram Credential Harvester   =")
    print("=          Objective: API Acquisition         =")
    print("=============================================")
    print("\n[INFO] Initializing headless browser environment...")

def get_credentials():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background. No GUI needed.
    options.add_argument("--log-level=3") # Suppress unnecessary console noise.
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 15)
        driver.get(TELEGRAM_URL)
        print("[INFO] Connection established with my.telegram.org.")
    except Exception as e:
        print(f"[FATAL] WebDriver initialization failed: {e}")
        print("[FATAL] Ensure Chrome is installed or check network connection.")
        return

    try:
        # --- Stage 1: Authentication ---
        phone_number = input("[PROMPT] Enter your full phone number (e.g., +15551234567): ")
        
        phone_input = wait.until(EC.presence_of_element_located((By.NAME, 'phone_number')))
        phone_input.send_keys(phone_number)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        print("[INFO] Phone number submitted. A code has been sent to your Telegram app.")

        # Manual input is a necessary evil for 2FA.
        confirmation_code = input("[PROMPT] Enter the confirmation code you received: ")
        code_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        code_input.send_keys(confirmation_code)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        print("[INFO] Authentication successful. Accessing API tools...")

        # --- Stage 2: Application Creation ---
        # Wait for the app creation form to be visible
        wait.until(EC.presence_of_element_located((By.ID, 'app_title')))
        
        driver.find_element(By.ID, 'app_title').send_keys(APP_TITLE)
        driver.find_element(By.ID, 'app_shortname').send_keys(SHORT_NAME)
        # Platform selection is required. We choose Desktop for simplicity.
        driver.find_element(By.ID, 'app_platform_desktop').click()
        driver.find_element(By.XPATH, '//button[contains(text(), "Create application")]').click()
        print("[INFO] Disposable application created.")

        # --- Stage 3: Credential Extraction ---
        print("[INFO] Locating and extracting credentials...")
        # Wait for the credentials to be displayed on the page
        api_id_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'App api_id')]/following-sibling::div/span/strong")))
        api_hash_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'App api_hash')]/following-sibling::div/span")))

        api_id = api_id_element.text
        api_hash = api_hash_element.text
        
        print("\n--- OPERATION COMPLETE ---")
        print(f"API ID:   {api_id}")
        print(f"API Hash: {api_hash}")
        print("--------------------------")

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during the operation: {e}")
        print("[ERROR] This could be due to an incorrect phone number, an invalid code, or a change in Telegram's website structure.")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("\n[INFO] Secure session terminated.")

if __name__ == '__main__':
    display_header()
    get_credentials()