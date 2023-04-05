from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize a Selenium browser instance
browser = webdriver.Chrome()

# Navigate to the website
browser.get("https://www.weather.go.kr/w/index.do")

# Wait for the page to load
browser.implicitly_wait(10)

# Wait for the element to become visible
dust_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cmp-cur-weather.cmp-cur-weather-air > ul > li:nth-child(2) > strong > span.air-lvv-wrap.air-lvv-2 > span")))

# Get the fine dust value
fine_dust = dust_element.text

# Print the fine dust value
print("Fine dust value:", fine_dust)

# Close the browser
browser.quit()


    