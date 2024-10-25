from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# Appium server URL
APPIUM = "http://127.0.0.1:4723"

# Desired capabilities for Android Chrome
CAPS = {
    "platformName": "Android",
    "browserName": "Chrome",
    "appium:options": {
        "platformVersion": "13",  # Adjust this to your device version if needed
        "deviceName": "RF8T40T905V",  # Change this to your device name
        "automationName": "UiAutomator2",
        "chromedriverVersion": "130.0.6723.69",
        "chromedriverExecutableDir": r"C:\Users\MahamKhurshid\.appium\node_modules\appium-uiautomator2-driver"
        # Correct path to the directory containing chromedriver.exe
    }
}

# Initialize Appium options and load capabilities
OPTIONS = AppiumOptions().load_capabilities(CAPS)

# Initialize WebDriver
driver = webdriver.Remote(
    command_executor=APPIUM,
    options=OPTIONS
)

# Function to confirm we are on the Amazon home page by checking the title
def confirm_amazon_home_page():
    try:
        expected_title = "Amazon.com.au: Shop online for Electronics, Apparel, Toys, Books, DVDs & more"
        actual_title = driver.title
        assert actual_title == expected_title, f"Page title mismatch! Expected: '{expected_title}', but got: '{actual_title}'"
        print("Confirmed: We are on the Amazon home page.")
    except Exception as e:
        print(f"Failed to confirm the Amazon home page: {e}")
        raise

# Function to change device orientation to landscape
def change_orientation_to_landscape():
    driver.orientation = "LANDSCAPE"
    print("Device orientation changed to landscape.")

# Function to change device orientation to portrait
def change_orientation_to_portrait():
    driver.orientation = "PORTRAIT"
    print("Device orientation changed back to portrait.")

# Retry logic to rerun test in case of failures
def run_test_with_retry(test_function, retries=3):
    for attempt in range(retries):
        try:
            test_function()  # Execute the test function
            print("Test passed successfully")
            break
        except Exception as e:
            print(f"Test failed on attempt {attempt + 1}/{retries}: {e}")
            if attempt == retries - 1:
                raise  # If it's the last attempt, raise the exception
            else:
                driver.get('https://www.amazon.com.au')  # Relaunch web for the retry

# Create explicit wait
wait = WebDriverWait(driver, 10)  # 10 seconds wait

# Test flow function
def test_flow():
    # Step 1: Navigate to Amazon website
    driver.get('https://www.amazon.com.au')
    print("Navigated to Amazon website.")
    confirm_amazon_home_page()

    # Step 2: Change orientation to landscape
    change_orientation_to_landscape()

    # Step 3: Change orientation to portrait
    change_orientation_to_portrait()
    time.sleep(2)

    # Step 4: Search for 'laptop'
    search_bar = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='nav-search-keywords']"))
    )
    search_bar.send_keys("laptop")

    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Go']"))
    )
    search_button.click()
    time.sleep(2)

    # Step 5: Scroll down until the "Add to Cart" button is found
    def scroll_until_add_to_cart():
        while True:
            try:
                add_to_cart_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'a-button-text') and text()='Add to cart'][1]"))
                )
                add_to_cart_button.click()
                print("Item added to cart successfully")
                break
            except NoSuchElementException:
                driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels
                time.sleep(2)

    scroll_until_add_to_cart()  # Call the scroll function

    # Step 6: Scroll up until the cart link is found and click it
    while True:
        try:
            cart_link = driver.find_element(By.XPATH, "//a[@id='nav-button-cart']")
            cart_link.click()
            print("Navigated to the cart page successfully :D")
            break
        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, -500);")  # Scroll up by 500 pixels
            time.sleep(2)

# Execute the test with retry logic
try:
    run_test_with_retry(test_flow)
except Exception as e:
    print(f"Test ultimately failed: {e}")
finally:
    driver.quit()  # Ensure driver quits properly
