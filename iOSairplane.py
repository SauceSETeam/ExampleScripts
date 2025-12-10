import time
from appium.webdriver.common.appiumby import AppiumBy

def toggle_ios_airplane_mode(driver):
    """
    Toggles Airplane Mode on iOS by automating the 'com.apple.Preferences' app.
    """
    print(" [iOS] Launching Settings App...")
    
    # 1. Launch Apple Settings
    driver.activate_app("com.apple.Preferences")
    time.sleep(2)
    
    # 2. Find the Airplane Mode Switch
    # It is located inside a Cell that has the text "Airplane Mode"
    try:
        xpath = '//XCUIElementTypeCell[.//XCUIElementTypeStaticText[@name="Airplane Mode"]]//XCUIElementTypeSwitch'
        switch = driver.find_element(AppiumBy.XPATH, xpath)
        
        # Optional: Check state (Value is '1' for On, '0' for Off)
        # current_val = switch.get_attribute("value")
        
        switch.click()
        print(" [iOS] Toggled Airplane Mode switch.")
        
    except Exception as e:
        print(f" [iOS] Failed to find switch: {e}")
        
    # 3. Handle potential system alerts (e.g., "Disconnecting Bluetooth?")
    # Some iOS versions pop up a warning when entering Airplane mode if BT was on.
    try:
        # A simple check for a 'Cancel' or 'OK' button if an alert exists
        alert_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
        if len(alert_buttons) > 0 and "Disconnect" in driver.page_source:
             alert_buttons[0].click() # Click the first button (usually OK)
    except:
        pass

    # 4. Return to your app
    # driver.activate_app("com.your.bundle.id")