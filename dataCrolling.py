import time
#동적크롤링(스크래핑)
from selenium import webdriver
from selenium.webdriver.common.by import By
#url연결
url = "https://www.weather.go.kr/w/index.do"
#Edge브라우저 및 get요청
browser = webdriver.Chrome()
browser.get(url)

#20초동안 창을 켜둬서 내가 원하는지역검색후에 가만히 두면 크롤링됨(시간변경가능)
time.sleep(10)
#지역
area = browser.find_element(By.CSS_SELECTOR, 'a.serch-area-btn.accordionsecond-tit').text
#온도
#temperature
temp = browser.find_element(By.CSS_SELECTOR, "span.tmp").text
temp = float(temp[:-1])

#최저온도
minTemp = browser.find_element(By.CSS_SELECTOR,'span.tmin').text

#최고온도
maxTemp = browser.find_element(By.CSS_SELECTOR,'span.tmax').text
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
#초미세먼지
ultraDust = browser.find_element(By.CSS_SELECTOR, 'span.air-lvv').get_attribute('textContent')
#미세먼지
dust = browser.find_element(By.CSS_SELECTOR,"div.cmp-cur-weather.cmp-cur-weather-air > ul > li:nth-child(2) > strong > span.air-lvv-wrap.air-lvv-1 > span").get_attribute('textContent')
#get_attribute 특정 값이나 서식 지정 정보를 추출하기 위해 get_attribute('textContent')를 사용해야 할 수도 있습니다.

#출력
print(f"선택지역:{area}")
print(f"온도:{temp}")
print(f"{maxTemp}")
print(f"{minTemp}")
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도: {humidity}")
print(f"바람: {wind}")
print(f"강수량: {rainfall}")
print(f"초미세먼지:{ultraDust}㎍/m³")
print(f"미세먼지:{dust}㎍/m³")

browser.quit()

"""
<ul>
  <li>
  <strong class="air-level val">
    <span class="air-lvv-wrap air-lvv-2">
      <small class="air-lvv">31</span>
      <small class="unit">m3</small>
  </strong>
  </li>
<ul/>
"""

"""
<div class="serch-area accordionsecond-wrap acco-on">
<a href="#" class="serch-area-btn accordionsecond-tit on" data-role="bookmark-selected" title="펼쳐짐" data-wide-code="4600000000" data-wide-name="전남" data-city-code="4682000000" data-city-name="해남군" data-dong-code="4682034000" data-dong-name="송지면" data-x="53" data-y="55" data-lat="34.2972777904718" data-lon="126.525759259436">전남 해남군 송지면</a>
  <div class="accordionsecond-con serch-con" style="display: block;">
      <div>
        <ul data-role="bookmark-holder"></ul>
      </div>
  </div>
</div>
"""
