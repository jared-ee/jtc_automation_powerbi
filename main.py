import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from workflow import *

def main():
    # Less than two arguments
    if len(sys.argv) < 2:
        print("Too few arguments. Provide the Mode [create, delete, ...]")
        return

    # More than two arguments indicates that this command involves the use of selenium
    if len(sys.argv) > 2:
        chrome_options = Options()
        driver = webdriver.Remote(
            command_executor='http://host.docker.internal:4444/wd/hub',
            options=chrome_options
        )
        try:
            driver.maximize_window()

            log_in_mode = sys.argv[2]
            if log_in_mode == 'cookie':
                cookie_flow(driver)
                time.sleep(1000)
            elif log_in_mode == 'auth':
                sign_in_flow(driver)
            else:
                print("Invalid Sign In Mode")
        finally:
            driver.quit()

    if len(sys.argv) == 2:
        mode = sys.argv[1]
        if mode == 'configure':
            configure_dashboard()
        else:
            print("Invalid Mode")
            return

if __name__ == "__main__":
    main()
