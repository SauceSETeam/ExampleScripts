import os
import sys
import warnings
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Suppress SSL warnings
warnings.filterwarnings("ignore", category=UserWarning)

def setup_sauce_labs_ios_driver():
    """
    Setup Sauce Labs driver using a Dummy App as the entry point, 
    then switching to the System Messages app.
    """
    options = AppiumOptions()
    
    # Standard Capabilities
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    
    # Entry Point: Use a Dummy App
    # We use the official Sauce Labs Demo App (public URL). But you can swap to your app if you like
    options.set_capability('appium:app', 'https://github.com/saucelabs/sample-app-mobile/releases/download/2.7.1/iOS.RealDevice.SauceLabs.Mobile.Sample.app.2.7.1.ipa')
    
    # Device Config
    options.set_capability('appium:deviceName', 'DevideID') # - PRIVATE DEVICE WITH SIM

    # Sauce Options
    sauce_options = {
        'username': os.environ.get('SAUCE_USERNAME'),
        'accessKey': os.environ.get('SAUCE_ACCESS_KEY'),
        'name': 'iOS Messages Test (Dummy App Entry)',
        'build': 'System App Test Build',
        # FIX: appiumVersion MUST be inside sauce:options
        'appiumVersion': 'latest' 
    }
    options.set_capability('sauce:options', sauce_options)
    
    sauce_url = 'https://ondemand.us-west-1.saucelabs.com/wd/hub'
    
    print("Starting Sauce Labs Session (Using Dummy App Entry)...")
    driver = webdriver.Remote(sauce_url, options=options)
    return driver

def send_ios_message(driver, recipient, message_text):
    try:
        # --- Switch from Dummy App to Messages App ---
        print("Session started. Switching to Messages App...")
        
        # Close the Dummy App
        try:
            driver.terminate_app('com.saucelabs.mydemoapp.rn')
        except:
            pass 
            
        # Activate Messages App
        driver.activate_app('com.apple.MobileSMS')
        
        # Proceed with Automation
        new_message_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, 'composeButton'
            ))
        )
        new_message_button.click()
        
        # Handle the Recipient Input
        recipient_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                AppiumBy.XPATH, "//XCUIElementTypeTextField[@name='To:']"
            ))
        )
        recipient_input.send_keys(recipient)
        
        # Handle 'Enter' on iOS Keyboard
        try:
            # Wait briefly to see if contact suggestion appears
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((
                     AppiumBy.XPATH, f"//XCUIElementTypeStaticText[@name='{recipient}']"
                ))
            ).click()
        except:
            # If no suggestion, hit Newline/Enter
            recipient_input.send_keys('\n')

        # Handle Message Body
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                AppiumBy.ACCESSIBILITY_ID, 'messageBodyField'
            ))
        )
        message_input.send_keys(message_text)
        
        # Click Send
        send_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                AppiumBy.ACCESSIBILITY_ID, 'sendButton'
            ))
        )
        send_button.click()
        
        print(f"Message successfully sent to {recipient}")
    
    except Exception as e:
        print(f"Error during execution: {e}")
        raise

def main():
    driver = None
    try:
        driver = setup_sauce_labs_ios_driver()
        send_ios_message(driver, 'ENTER PHONE NUMBER', 'Testing Text Feature!')
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        if driver:
            print(f"Sauce Link: https://app.saucelabs.com/tests/{driver.session_id}")
            driver.quit()

if __name__ == "__main__":
    main()