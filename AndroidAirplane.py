import time
from appium.webdriver.common.appiumby import AppiumBy

def toggle_android_airplane_mode(driver):
    """
    Toggles Airplane Mode on Android using the Settings Intent.
    Works on Real Devices (Sauce Labs/BrowserStack) where 'driver.toggle_airplane_mode()' fails.
    """
    print(" [Android] Opening Airplane Mode Settings...")
    
    # 1. Open the specific Airplane Mode settings screen
    driver.execute_script('mobile: shell', {
        'command': 'am start',
        'args': ['-a', 'android.settings.AIRPLANE_MODE_SETTINGS']
    })
    
    time.sleep(2) # Wait for screen transition
    
    # 2. Find the toggle switch
    # On most Android versions, this is the only/first switch on this specific screen
    try:
        switch = driver.find_element(AppiumBy.XPATH, "//android.widget.Switch")
        
        # Optional: Check current state (Text is often 'ON' or 'OFF')
        # is_currently_on = switch.text == 'ON' 
        
        switch.click()
        print(" [Android] Toggled Airplane Mode switch.")
        
    except Exception as e:
        print(f" [Android] Failed to find switch: {e}")

    # 3. Wait briefly for network to drop/reconnect
    time.sleep(3)

    # 4. Return to your app
    # driver.activate_app("com.your.package.name")