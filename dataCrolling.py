#정적크롤링
import requests
from bs4 import BeautifulSoup



#동적크롤링
from selenium import webdriver
from selenium.webdriver.common.by import By

#url연결
url = "https://www.weather.go.kr/w/index.do"
#Edge브라우저 및 get요청
browser = webdriver.Edge()
browser.get(url)
#기상청에서 class가 tmp인걸 따옴(온도)
temp = browser.find_elements(By.CLASS_NAME, "tmp")
#체감온도
actualTemp = browser.find_elements(By.CLASS_NAME,'chill')
#습도 바람 1시간강수량
humidity = browser.find_element(By.CSS_SELECTOR, '.val')


#무조건반복문으로 따와야지만 텍스트로 내보내주는것같음
#온도
for temp in temp:
  temp = temp.text
print("온도:", temp)
#체감온도
if actualTemp:
  actualTemp = actualTemp[0].text
  actualTemp = actualTemp.replace("체감","").replace("(", "").replace(")", "")
  print("체감온도:",actualTemp)
#습도
#humidity
if humidity:
  humidity = humidity.text
  print("습도:", humidity)




browser.quit()



