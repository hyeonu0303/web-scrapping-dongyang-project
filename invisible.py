"""
사용모듈
1.seleium

"""
#정적크롤링

#동적크롤링
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

options=Options()
options.add_argument('--headless')
url="https://www.weather.go.kr/w/index.do"
#엣지브라우저 와 요청
browser=webdriver.Edge(options=options)
browser.get(url)

#온도
temp = browser.find_element(By.CLASS_NAME, "tmp").text
#체감온도
actualTemp = browser.find_element(By.CLASS_NAME, 'chill').text.replace("체감", "").replace("(", "").replace(")", "")
#어제보다 몇도높은지 부분 스크래핑
temp_diff = browser.find_element(By.CSS_SELECTOR, '.wrap-1>.w-txt').text

#wrap-2>li>val이 3개여서 items에담음
items = browser.find_elements(By.CSS_SELECTOR, '.wrap-2.no-underline li')
#습도
humidity = items[0].find_element(By.CLASS_NAME, 'val').text
#바람
wind = items[1].find_element(By.CLASS_NAME, 'val').text
#강수량
rainfall = items[2].find_element(By.CLASS_NAME, 'val').text

#온도
print(f"온도:{temp}")
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도:{humidity}")
print(f"바람:{wind}")
print(f"강수량:{rainfall}")

browser.quit()