from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://www.weather.go.kr/w/index.do')

wait = WebDriverWait(browser, 10)

# 지역 검색 창 열기
search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-btn')))
search_button.click()

# 시/도 선택
sido_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sido')))
sido_select.click()
sido_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="11"]')))
sido_option.click()

# 시/군/구 선택
sigungu_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sigungu')))
sigungu_select.click()
sigungu_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="110"]')))
sigungu_option.click()

# 읍/면/동 선택
dong_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#dong')))
dong_select.click()
dong_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="1114059000"]')))
dong_option.click()

# 검색 버튼 클릭
search_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
search_submit.click()

# 날씨 정보 텍스트 가져오기
weather_info_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.now_weather1')))
weather_info_text = weather_info_element.text

print(weather_info_text)