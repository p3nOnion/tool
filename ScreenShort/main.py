from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from concurrent.futures import ThreadPoolExecutor
import requests

def capture_screenshot(url):
    url=f"https://{url.strip()}"
    try:
        # Check the HTTP response status before proceeding
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Skipping {url} - Non-200 status code: {response.status_code}")
            return

        # Create a new WebDriver instance
        local_driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the current URL
        local_driver.get(url)
        wait = WebDriverWait(local_driver, 30)
        # body_tags = wait.until(lambda local_driver: local_driver.find_elements(By.TAG_NAME, 'body') if local_driver else None)
        # Wait for the 'complete' state of the document
        # wait = WebDriverWait(local_driver, 10)
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Ensure the body is present
        # wait.until(EC.presence_of_element_located((By.XPATH, '//body[contains(@class, "loaded")]')))  # Adjust the XPath as needed

        # Print some debug information
        print(f"Page title: {local_driver.title}")
        print(f"Current URL: {local_driver.current_url}")

        # Extract the filename from the URL
        filename = urlparse(url).netloc + urlparse(url).path

        # Replace special characters in the filename
        filename = filename.replace('/', '_').replace('.', '_')

        # Take a screenshot and save it with the extracted filename
        screenshot_filename = f'out/screenshot_{filename}.png'
        local_driver.save_screenshot(screenshot_filename)
        print(f'Screenshot captured for {url}. Saved as {screenshot_filename}')

    except TimeoutException as e:
        print(f'Timeout error for {url}: {str(e)}')

    except WebDriverException as e:
        print(f'WebDriver error for {url}: {str(e)}')

    except Exception as e:
        print(f'Error capturing screenshot for {url}: {str(e)}')

    finally:
        # Print debug information
        # print(f"Finally block - local_driver: {local_driver}")

        # Close the WebDriver instance after capturing the screenshot
        if local_driver:
            local_driver.quit()

# List of URLs to capture screenshots for
url_list = ['upl.dev.df.msb.com.vn']
f = open('domain.txt','r')
# url_list= f.readlines()

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Number of threads to use
num_threads = 3

# Use ThreadPoolExecutor to run the capture_screenshot function for each URL in parallel
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    executor.map(capture_screenshot, url_list)
