import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

def android_system_toggles(driver):
    """
    Toggles Wi-Fi and Airplane Mode on Android Real Devices
    using direct Activity Intents.
    """
    
    # --- Toggle Wi-Fi ---
    print("Opening Wi-Fi Settings...")
    # 'mobile: shell' works on Sauce Labs to execute ADB commands
    driver.execute_script('mobile: shell', {
        'command': 'am start',
        'args': ['-a', 'android.settings.WIFI_SETTINGS']
    })
    
    time.sleep(2) # Wait for animation
    
    # Locate the master switch. 
    # Note: On most Androids, the master switch is the first/only switch widget on this screen.
    wifi_switch = driver.find_element(AppiumBy.XPATH, "//android.widget.Switch")
    
    # Optional: Check state
    # current_state = wifi_switch.text  # Often 'ON' or 'OFF'
    
    wifi_switch.click()
    print("Wi-Fi Toggled.")

    # --- Toggle Airplane Mode ---
    print("Opening Airplane Mode Settings...")
    driver.execute_script('mobile: shell', {
        'command': 'am start',
        'args': ['-a', 'android.settings.AIRPLANE_MODE_SETTINGS']
    })
    
    time.sleep(2)
    
    airplane_switch = driver.find_element(AppiumBy.XPATH, "//android.widget.Switch")
    airplane_switch.click()
    print("Airplane Mode Toggled.")

    # --- Return to App ---
    # Replace with your actual package name
    driver.activate_app("com.your.company.app")