from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Function to scrape market data
def scrape_market_data(driver):
    # Wait until the page is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'commodity_id')))


    # Wait for the "select a region" dropdown to be present
    select_commodity_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'commodity_id'))
    )

    # Select water drum 200L
    select_commodity = Select(select_commodity_dropdown)
    select_commodity.select_by_visible_text('Water Drum 200L')

    # Click "Get Market Data" button
    submit_button = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'btnGetData'))
    )
    submit_button.click()

    # Wait until the data is loaded
    time.sleep(3)

    # Select goat prices
    select_commodity.select_by_visible_text('Goat Prices')

    # Click "Get Market Data" button
    submit_button.click()

    # Wait until the data is loaded
    time.sleep(3)

    # Parse the HTML
    #soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract and print the market data
    #market_data = soup.find('table', {'class': 'table'}).get_text()
    #print(market_data)

# Initialize the WebDriver (Chrome)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome()


#LOGIN

# Navigate to the login page
driver.get("https://fsnau.org/ids/index.php?msg=You%20tried%20to%20access%20the%20IDS%20without%20logging%20in%20first.%20Please%20log%20in%20below:")

# Fill in login credentials
username = 'USERNAME'
password = 'PASSWORD'

# Wait for the username field to be visible
username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'username'))
)
username_field.send_keys(username)

# Wait for the password field to be visible
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'password'))
)
password_field.send_keys(password)

# Find and click the submit button
submit_button = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'btnLogin'))
)
submit_button.click()

#SCRAPE


# Navigate to the desired page after successful login
driver.get('https://fsnau.org/ids/markets/index.php')

# Wait until the page is loaded
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'region_id')))

# Wait for the "select a region" dropdown to be present
select_region_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'region_id'))
)

# Select the "select a region" dropdown
select_region = Select(select_region_dropdown)

# Loop through each option in the "select a region" dropdown
for option in select_region.options:
    # Select the region
    select_region.select_by_visible_text(option.text)

    # Click "Get Market Data" button for water drum 200L
    scrape_market_data(driver)

    # Click "Get Market Data" button for goat prices
    scrape_market_data(driver)

# Close the WebDriver
driver.quit()
