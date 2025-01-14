import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, WebDriverException, NoSuchElementException
import time

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"..\chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def accept_cookies(self):
        try:
            cookie_button = self.find_element(By.CSS_SELECTOR, '[id="onetrust-accept-btn-handler"]')
            cookie_button.click()
        except Exception as e:
            print("No cookie popup detected or an error occurred:", e)


    def reject_offer(self):
        """Handle the deal popup if it appears."""
        try:
            # Check if there are any open browser windows
            if len(self.window_handles) > 0:
                close_button = WebDriverWait(self, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 f4552b6561"]'))
                )
                if close_button and close_button.is_displayed():
                    close_button.click()
                    print("Deal popup closed.")
                else:
                    print("Close button is not visible.")
            else:
                print("No open browser windows found.")
        except TimeoutException:
            print("No deal popup detected.")
        except NoSuchWindowException:
            print("Browser window is not available.")
        except AttributeError as e:
            print(f"Element is not valid or has gone stale: {e}")
        except WebDriverException as e:
            print(f"An unexpected WebDriver exception occurred: {e}")



    def change_currency(self, currency='USD'):
        self.accept_cookies()
        self.reject_offer()

        """Change the currency to the specified value."""
        try:
            # Open the currency picker
            currency_element = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-controls="header_currency_picker"]'))
            )
            currency_element.click()
            print("Currency picker opened.")

            # Select the desired currency
            currency_option = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'Picker_selection-text')]/div[text()='{currency}']"))
            )
            currency_option.click()
            print(f"Currency changed to {currency}.")
        except TimeoutException:
            print("Currency picker or option not found.")
        except NoSuchElementException:
            print("The specified currency option was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        self.reject_offer()
    
    def select_destination(self, destination):
        try:
            # Find the search box, clear it, and enter the destination
            search_box = self.find_element(By.CSS_SELECTOR, '[name="ss"]')
            search_box.clear()
            search_box.send_keys(destination)
            print(f"Destination '{destination}' entered.")

            # Wait for 1 second to allow the autocomplete suggestions to update
            time.sleep(1)

            # Select the first result from the updated autocomplete suggestions
            first_result = self.find_element(By.CSS_SELECTOR, '[id="autocomplete-result-0"]')
            first_result.click()
            print("First autocomplete result clicked.")
        except Exception as e:
            print(f"An error occurred while selecting the destination: {e}")
