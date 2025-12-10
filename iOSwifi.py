import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

def ios_system_toggles(driver):
    """
    Toggles Wi-Fi and Airplane Mode on iOS Real Devices
    by interacting with the com.apple.Preferences UI.
    """
    
    my_app_bundle_id = "com.your.company.app"

    # --- Toggle Airplane Mode ---
    print("Launching Settings for Airplane Mode...")
    driver.activate_app("com.apple.Preferences")
    time.sleep(1)
    
    # Airplane Mode is on the main settings list.
    # We find the Cell containing the text "Airplane Mode", then find the Switch inside it.
    airplane_xpath = '//XCUIElementTypeCell[.//XCUIElementTypeStaticText[@name="Airplane Mode"]]//XCUIElementTypeSwitch'
    airplane_switch = driver.find_element(AppiumBy.XPATH, airplane_xpath)
    
    airplane_switch.click()
    print("Airplane Mode Toggled.")
    
    # --- Toggle Wi-Fi ---
    
    # Restart Settings to ensure we are at the root menu (clean state)
    driver.terminate_app("com.apple.Preferences")
    driver.activate_app("com.apple.Preferences")
    
    print("Navigating to Wi-Fi Settings...")
    # Click the "Wi-Fi" menu item
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Wi-Fi").click()
    time.sleep(1)
    
    # Find the main Wi-Fi toggle switch
    # On the Wi-Fi specific page, it is usually the first switch present
    wifi_switch = driver.find_element(AppiumBy.CLASS_NAME, "XCUIElementTypeSwitch")
    
    # Optional: Get current value (1 = On, 0 = Off)
    # val = wifi_switch.get_attribute("value")
    
    wifi_switch.click()
    print("Wi-Fi Toggled.")

    # --- Return to App ---
    driver.activate_app(my_app_bundle_id)