import time as ostime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
DEFAULT_TIMEOUT = 60


# Wait for Element to Appear
def wait_xpath(driver, element, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, element)))

# Check if an element exists
def check_exists(driver, element, value, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    text = wait.until(EC.presence_of_element_located((By.XPATH, element)))
    if text == value: return true
    return False

# Scroll
def scroll(driver, path):
    wait = WebDriverWait(driver, time)
    scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, element)))
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", scrollable_div)

# Hover
def hover_xpath(driver, path, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
    actions = ActionChains(driver)
    actions.move_to_element(button).perform()

# Click
def click_text(driver, text, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), {text})]")
    ))
    button.click()

def click_xpath(driver, path, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
    button.click()
    #button = wait.until(EC.presence_of_element_located((By.XPATH, path)))
    #driver.execute_script("arguments[0].click();", button)

# Populate fields
def populate_xpath(driver, content, path, enter=False, delay=0, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    field = wait.until(EC.presence_of_element_located((By.XPATH, path)))
    field.clear()
    if enter:
        field.send_keys(content, Keys.ENTER)
    else:
        field.send_keys(content)

# Select fields
def select_element(driver, response, element, time=DEFAULT_TIMEOUT):
    wait = WebDriverWait(driver, time)
    element = wait.until(EC.presence_of_element_located((By.XPATH, element))) 
    select = Select(element)
    select.select_by_visible_text(response)
