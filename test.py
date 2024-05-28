from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def formAutomation(form:any):
        # Replace with the path to your WebDriver
    webdriver_path = './chromedriver/chromedriver.exe'

    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Replace with the URL of your Google Form
    form_url = form['url']

    # Open the Google Form
    driver.get(form_url)

    # Wait for the form to load
    time.sleep(0.30)


    # Find all text input elements (short answer and paragraph fields)
    text_input_elements = driver.find_elements(By.XPATH, '//input[@type="text"] | //textarea')

    for i, input_element in enumerate(text_input_elements):
        try:
            input_element.send_keys(form['fields'][i])
        except Exception as e:
            print(f"Error: {e}")
            continue

    button_divs = driver.find_elements(By.XPATH, '//div[@role="button"]')
    # Click the first button div found
    if button_divs:
        try:
            button_divs[0].click()
            print("Clicked on the button")
        except Exception as e:
            print(f"Error clicking the button: {e}")
    else:
        print("No button divs found")

    # Close the WebDriver
    driver.quit()

