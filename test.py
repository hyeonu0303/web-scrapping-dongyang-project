import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
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
time.sleep(15)
#지역
area = browser.find_element(By.CSS_SELECTOR, 'a.serch-area-btn.accordionsecond-tit').text
#온도
temp = browser.find_element(By.CSS_SELECTOR,"span.tmp").text
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
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("UIdesign.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.area1 = self.findChild(QLabel, "area1")
        self.area1.setText(area)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

    