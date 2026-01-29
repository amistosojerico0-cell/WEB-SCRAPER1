from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# -------------------------
# Setup Chrome WebDriver
# -------------------------
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if you want to run without opening the browser
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# -------------------------
# Open Website
# -------------------------
driver.get("https://example.com")  # Replace with your target URL

# -------------------------
# Wait for main container
# -------------------------
wait = WebDriverWait(driver, 10)
try:
    # Wait until at least one item loads
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product")))  # Use correct selector
except:
    print("Items not found. Check CSS selector or page load.")
    driver.quit()
    exit()

# -------------------------
# Optional: Click "Load more" button if exists
# -------------------------
try:
    button = driver.find_element(By.CSS_SELECTOR, "button.load-more")  # Update selector
    button.click()
    time.sleep(2)  # wait for new items to load
except:
    print("Load more button not found. Continuing...")

# -------------------------
# Scroll to bottom to load all items
# -------------------------
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for new content
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# -------------------------
# Collect links or items
# -------------------------
items = []
all_elements = driver.find_elements(By.CSS_SELECTOR, "div.product")  # Replace with correct item container
for el in all_elements:
    title = el.text  # Or use el.find_element(By.TAG_NAME, "h2").text if inside
    try:
        price = el.find_element(By.CSS_SELECTOR, "span.price").text
    except:
        price = "N/A"
    items.append({"title": title, "price": price})

# -------------------------
# Save to CSV
# -------------------------
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "price"])
    for item in items:
        writer.writerow([item["title"], item["price"]])

# -------------------------
# Optional: Print links
# -------------------------
for link in driver.find_elements(By.TAG_NAME, "a"):
    href = link.get_attribute("href")
    if href:
        print(link.text, href)

# -------------------------
# Close the browser
# -------------------------
driver.quit()
