import os
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests

# List of names to search for
names = [
    "B.J. Penn", "Royce Gracie", "Antonio Rodrigo Nogueira", "Dominick Cruz", "Max Holloway",
    "Junior Dos Santos", "Frankie Edgar", "Henry Cejudo", "Michael Bisping", "Randy Couture",
    "Kamaru Usman", "Alistair Overeem", "Dan Henderson", "Matt Hughes", "Chuck Liddell",
    "José Aldo", "Conor McGregor", "Israel Adesanya", "Khabib Nurmagomedov",
    "Demetrious Johnson", "Daniel Cormier", "Stipe Miocic", "Georges St-Pierre",
    "Jon Jones", "Anderson Silva"
]

# Set up the WebDriver (make sure to download the correct driver for your browser)
chrome_driver_path = "/Users/varunwadhwa/Downloads/chromedriver-mac-arm64/chromedriver"  # Replace with the path to your ChromeDriver if necessary
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

def download_image(image_url, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)

# Create a directory to save the images
if not os.path.exists('ufc_images'):
    os.makedirs('ufc_images')

# URL to the UFC search page
url = "https://www.ufc.com/search"

for name in names:
    driver.get(url)
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    if iframe:
        # Switch to the iframe
        driver.switch_to.frame(iframe)
    div = driver.find_element(By.CLASS_NAME,'yxt-SearchBar')
    search_box = driver.find_element(By.CLASS_NAME,'yxt-SearchBar-form')
    input_element = search_box.find_element(By.TAG_NAME, "input")
    # except Exception as e:
    #     print(f"Could not download image for {name}: {e}")
    input_element.send_keys(name)
    input_element.send_keys(Keys.RETURN)
    time.sleep(3)  # Allow time for the page to load and display results
        

    try:
        div = driver.find_element(By.CLASS_NAME, 'HitchhikerProductProminentImage-imgWrapper')
        first_image = div.find_element(By.TAG_NAME, "img")  # Adjust the selector as needed
        image_url = first_image.get_attribute("src")
        download_image(image_url, os.path.join('ufc_images', f"{name}.png"))
        print(f"Downloaded image for {name}")
    except Exception as e:
        print(f"Could not download image for {name}: {e}")

driver.quit()
