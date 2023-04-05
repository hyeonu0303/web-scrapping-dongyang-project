import time
# 정규식(regular expression) 쉽게 문자열에서 패턴에 해당하는 부분을 추출
import re
# 동적크롤링(스크래핑)
from selenium import webdriver
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
import sys

# url연결
url = "https://www.weather.go.kr/w/index.do"
# Edge브라우저 및 get요청
browser = webdriver.Chrome()
browser.get(url)

#'-'문자를 숫자0으로 반환하는함수
def extract_number(string):
    # 정규식 패턴으로 숫자 추출
    numbers = re.findall(r'\d+', string)
    if numbers:
        # 추출된 숫자가 있다면 첫 번째 숫자 반환
        return float(numbers[0])
    else:
        # 추출된 숫자가 없다면 0 반환
        return 0

# 20초동안 창을 켜둬서 내가 원하는지역검색후에 가만히 두면 크롤링됨(시간변경가능)
time.sleep(5)


# 지역
area = browser.find_element(
    By.CSS_SELECTOR, 'a.serch-area-btn.accordionsecond-tit').text
# 온도
temp = browser.find_element(By.CSS_SELECTOR, "span.tmp").text
# 온도를 실수형으로 전환


# 최저온도
minTemp = browser.find_element(By.CSS_SELECTOR, 'span.tmin').text

# 최고온도
maxTemp = browser.find_element(By.CSS_SELECTOR, 'span.tmax').text
# 체감온도
actualTemp = browser.find_element(By.CLASS_NAME, 'chill').text.replace(
    "체감", "").replace("(", "").replace(")", "")
# 어제보다 몇도높은지 부분 스크래핑
temp_diff = browser.find_element(By.CSS_SELECTOR, '.wrap-1>.w-txt').text

# wrap-2>li>val이 3개여서 items에담음
items = browser.find_elements(By.CSS_SELECTOR, '.wrap-2.no-underline li')

# 습도
humidity_str = items[0].find_element(By.CLASS_NAME, 'val').text
humidity = float(re.findall('\d+', humidity_str)[0])

# 바람
wind_str = items[1].find_element(By.CLASS_NAME, 'val').text
wind = float(re.findall('\d+', wind_str)[0])

# 강수량
rainfall_str = items[2].find_element(By.CLASS_NAME, 'val').text
# rainfall = float(re.findall('\d+', rainfall_str)[0])
rainfall = extract_number(rainfall_str)

# 초미세먼지
ultraDust = int(browser.find_element(By.CSS_SELECTOR,
                'span.air-lvv').get_attribute('textContent'))
# ultraDust = extract_number(ultraDust)
# 미세먼지
dust = int(browser.find_element(By.CSS_SELECTOR,
          "div.cmp-cur-weather.cmp-cur-weather-air > ul > li:nth-child(2) > strong > span.air-lvv-wrap.air-lvv-1 > span").get_attribute('textContent'))




# 현재 온도 정보에 따른 출력
""" def fTemp(temp):
    if temp > 30.0:
        return "오늘은 매우 더워요! 더위 조심하세요."
    elif temp > 25.0:
        return "오늘은 더운 날씨예요. 물 많이 마시고 적당히 움직이세요."
    elif temp > 20.0:
        return "오늘은 날씨가 쾌적해요. 산책하기 좋은 날씨네요."
    else:
        return "오늘은 날씨가 조금 쌀쌀해요. 따뜻하게 입고 다니세요."
 """
# 현재 습도 정보에 따른 출력
def fHumidity(humidity):
    if humidity >= 30 and humidity <= 60:
        return "습도가 적정합니다."
    elif humidity < 30:
        return "습도가 너무 낮습니다. 가습기를 사용하는 것이 좋습니다."
    elif humidity > 60:
        return "습도가 너무 높습니다. 제습기를 사용하는 것이 좋습니다."
    else:
        return "자료없음"

# 현재 바람 정보에 따른 출력
def fWind(wind):
    if wind < 0.3:
        return "이정도면 바람이 안부네요!" 
    elif wind >= 0.3 and wind <= 1.5:
        return "실바람이 불어요!" 
    elif wind >= 1.6 and wind <= 3.3:
        return "남실바람이 불어요!" 
    elif wind >= 3.4 and wind <= 5.4:
        return "산들바람이 불어요!" 
    else:
        return "바람이 강하니 외출을 자제해주세요!" 

# 현재 강수량 정보에 따른 출력
def fRainfall(rainfall):
    if rainfall == 0 :
        return "오늘은 비가 안와요!" 
    elif rainfall < 3.0:
        return "약한 비가 와요!" 
    elif rainfall >= 3.0 and rainfall < 15.0:
        return "적당한 비가 내려요!" 
    elif rainfall >= 15.0:
        return "강한 비가 내리니 외출을 자제하세요!" 
    elif rainfall >= 30.0:
        return "매우 강한 비가 내리니 외출하지마세요!" 
    else :
        print("자료없음")

# 현재 초미세먼지 정보에 따른 출력
def fUltra(ultraDust):
    if ultraDust >= 0:
        return "좋음"
    elif ultraDust >= 16:
        return "보통"
    elif ultraDust >= 36:
        return "나쁨"
    elif ultraDust >= 76:
        return "매우 나쁨"
    else:
        return "자료없음"

# 현재 미세먼지 정보에 따라 출력
def fDust(dust):
    if dust >= 0:
        return "좋음"
    elif dust >= 31:
        return "보통"
    elif dust >= 81:
        return "나쁨"
    elif dust >= 151:
        return "매우나쁨"
    else:
        return "자료없음"

# 총평

# 온도 강수량 습도 미세먼지


# 출력

print(f"선택지역:{area}")
print(f"Temperature:{temp}")
print(f"{maxTemp}")
print(f"{minTemp}")
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도: {humidity} %", end=' / ')
# fHumidity()
print(f"바람: {wind} m/s", end=' / ')
# fWind()
print(f"강수량: {rainfall} mm", end=' / ')
print(f"초미세먼지:{ultraDust}㎍/m³", end=' / ')
print(f"미세먼지:{dust}㎍/m³", end=' / ')

browser.quit()
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("UIdesign.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #지역명
        self.area_data = self.findChild(QLabel, "area_data")
        self.area_data.setText(area)
        #어제보다 몇도높은지부분
        self.temp_diff_data = self.findChild(QLabel, "temp_diff_data")
        self.temp_diff_data.setText(temp_diff)
        #현재온도
        self.currentTemp = self.findChild(QLabel, "currentTemp")
        self.currentTemp.setText(temp)
        #최고온도
        self.maxTemp = self.findChild(QLabel, "maxTemp")
        self.maxTemp.setText(maxTemp)
        #최저온도
        self.minTemp = self.findChild(QLabel, "minTemp")
        self.minTemp.setText(minTemp)
        #체감온도
        self.actTemp = self.findChild(QLabel, "actTemp")
        self.actTemp.setText(actualTemp)
        #습도
        self.fhumidity_data = self.findChild(QLabel, "fhumidity_data")
        self.fhumidity_data.setText(str(humidity))
        #습도멘트
        self.fhumidity_comm = self.findChild(QLabel, "fhumidity_comm")
        self.fhumidity_comm.setText(fHumidity(humidity))
        #바람
        self.wind_data = self.findChild(QLabel, "wind_data")
        self.wind_data.setText(str(wind))
        #바람멘트
        self.wind_comm = self.findChild(QLabel, "wind_comm")
        self.wind_comm.setText(fWind(wind))
        #강수량
        self.rain_data = self.findChild(QLabel, "rain_data")
        self.rain_data.setText(str(rainfall))
        #강수량멘트
        self.rain_comm = self.findChild(QLabel, "rain_comm")
        self.rain_comm.setText(fRainfall(rainfall))
        #미세먼지데이터
        self.dust_data = self.findChild(QLabel, "dust_data")
        self.dust_data.setText(str(dust))
        #미세먼지멘트
        self.dust_comm = self.findChild(QLabel, "dust_comm")
        self.dust_comm.setText(fDust(dust))
        #초미세먼지데이터
        self.udust_data = self.findChild(QLabel, "udust_data")
        self.udust_data.setText(str(ultraDust))
        #초미세먼지멘트
        self.udust_comm = self.findChild(QLabel, "udust_comm")
        self.udust_comm.setText(fUltra(ultraDust))
        #총데이터




if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
