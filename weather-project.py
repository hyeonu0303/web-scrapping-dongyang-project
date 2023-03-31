import requests
from bs4 import BeautifulSoup

#날씨 크롤링
# 체감온도 몇도이상에 바람 몇m/s이상이면 덥고 앞머리주의!
def crollingWeather():
    print('[오늘날씨]')
    url = "https://www.weather.go.kr/w/index.do"
    res = requests.get(url)
    #문제가 생길시 알려줌
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")
    temp = soup.find("title").get_text()
    print(temp)


crollingWeather()

#웹페이지 테스트 자동화 selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get("https://www.weather.go.kr/w/index.do")

wait = WebDriverWait(browser, 1)
temp_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tmp")))
temp = temp_element.text
print(f"현재온도:{temp}")
# browser.quit()